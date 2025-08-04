from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, flash, jsonify
import os
import json
import re
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey@#69'  # Change to a strong key in production

# Load LMS title from config
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))
with open(CONFIG_PATH) as f:
    config = json.load(f)
LMS_TITLE = config.get("lms_title", "My LMS")

# Set base directory and course paths file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COURSE_PATHS_FILE = os.path.join(BASE_DIR, "course_paths.txt")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")
IMPORTED_FILE = os.path.join(BASE_DIR, "imported_courses.json")

# Load progress and imported courses with error handling
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        try:
            progress_data = json.load(f)
        except json.JSONDecodeError:
            progress_data = {}
else:
    progress_data = {}

if os.path.exists(IMPORTED_FILE):
    with open(IMPORTED_FILE) as f:
        try:
            imported_courses = json.load(f)
        except json.JSONDecodeError:
            imported_courses = []
else:
    imported_courses = []

def load_course_paths():
    """Load course paths from the text file"""
    courses = {}
    
    # Create the file with example content if it doesn't exist
    if not os.path.exists(COURSE_PATHS_FILE):
        with open(COURSE_PATHS_FILE, 'w') as f:
            f.write("# Course Paths Configuration\n")
            f.write("# Add your course paths below, one per line\n")
            f.write("# Format: Course Name = /path/to/course/directory\n")
            f.write("# Example:\n")
            f.write("# Python Basics = /home/user/courses/python-basics\n")
            f.write("# Web Development = C:\\Courses\\WebDev\n")
            f.write("# Data Science = /media/courses/data-science\n")
        return courses
    
    try:
        with open(COURSE_PATHS_FILE, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse course name and path
                if '=' in line:
                    course_name, course_path = line.split('=', 1)
                    course_name = course_name.strip()
                    course_path = course_path.strip()
                    
                    # Expand environment variables and user home directory
                    course_path = os.path.expandvars(os.path.expanduser(course_path))
                    
                    # Check if the path exists
                    if os.path.exists(course_path) and os.path.isdir(course_path):
                        courses[course_name] = course_path
                    else:
                        print(f"Warning: Course path '{course_path}' for '{course_name}' does not exist (line {line_num})")
                else:
                    print(f"Warning: Invalid format on line {line_num}: '{line}'. Expected format: 'Course Name = /path/to/course'")
    
    except Exception as e:
        print(f"Error reading course paths file: {e}")
        return {}
    
    return courses

# Sorting helper
def sort_key(name):
    match = re.match(r'^\[?(\d+(?:\.\d+)*)(?=[\]\s\.-])?', name)
    if match:
        try:
            return [float(x) for x in match.group(1).split('.')]
        except:
            pass
    return [float('inf')]

# Helper to flatten the course structure to a list of videos
def _flatten_videos(structure):
    videos = []
    for item in structure:
        if item['type'] == 'video':
            videos.append(item)
        elif item['type'] == 'folder' and 'children' in item:
            videos.extend(_flatten_videos(item['children']))
    return videos

# Recursively build course tree with consistent IDs
def get_course_structure(course_path, course_name):
    if not os.path.exists(course_path) or not os.path.isdir(course_path):
        return []
    
    items = []
    try:
        # Pass the course root path down for relpath calculation
        def _build_tree(current_dir, course_root):
            tree_items = []
            for entry in sorted(os.listdir(current_dir), key=sort_key):
                full_path = os.path.join(current_dir, entry)
                
                if os.path.isdir(full_path):
                    children = _build_tree(full_path, course_root)
                    if children: # Only add folders that contain items
                        tree_items.append({
                            "type": "folder",
                            "name": entry,
                            "children": children
                        })
                elif entry.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".m4v", ".webm", ".flv", ".wmv", ".mpeg", ".mpg")):
                    rel_path = os.path.relpath(full_path, course_root).replace("\\", "/")
                    video_id = f"{course_name}/{rel_path}"
                    tree_items.append({
                        "type": "video",
                        "name": entry,
                        "full_path": full_path,
                        "id": video_id
                    })
            return tree_items

        items = _build_tree(course_path, course_path)

    except PermissionError:
        print(f"Permission denied accessing: {course_path}")
    except Exception as e:
        print(f"Error reading directory {course_path}: {e}")
    
    return items

@app.route('/login', methods=['GET', 'POST'])
def login():
    credentials = config.get("credentials", {})
    valid_user = credentials.get("username")
    valid_pass = credentials.get("password")

    # If credentials are missing, disable login
    if not valid_user or not valid_pass:
        session['user'] = "public"
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == valid_user and password == valid_pass:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', lms_title=LMS_TITLE)

# Homepage
@app.route('/')
def home():
    credentials = config.get("credentials", {})
    valid_user = credentials.get("username")
    valid_pass = credentials.get("password")

    # If login is required and user not logged in
    if (valid_user and valid_pass) and 'user' not in session:
        return redirect(url_for('login'))

    course_paths = load_course_paths()
    courses_with_progress = []

    for name, path in course_paths.items():
        structure = get_course_structure(path, name)
        all_videos = _flatten_videos(structure)
        
        total_count = len(all_videos)
        watched_count = sum(1 for video in all_videos if progress_data.get(video['id']))
        
        progress = int((watched_count / total_count * 100)) if total_count > 0 else 0
        
        courses_with_progress.append({
            "name": name,
            "progress": progress
        })
    
    return render_template("index.html", courses=courses_with_progress, imported=imported_courses, lms_title=LMS_TITLE)

# Course view
@app.route('/course/<path:course_name>')
def course_page(course_name):
    credentials = config.get("credentials", {})
    valid_user = credentials.get("username")
    valid_pass = credentials.get("password")

    if (valid_user and valid_pass) and 'user' not in session:
        return redirect(url_for('login'))

    # Load course paths and find the requested course
    course_paths = load_course_paths()
    
    if course_name not in course_paths:
        flash('Course not found!', 'danger')
        return redirect(url_for('home'))
    
    folder_path = course_paths[course_name]
    course_structure = get_course_structure(folder_path, course_name)

    first_video_obj = _flatten_videos(course_structure)[0] if _flatten_videos(course_structure) else None

    first_video_path = first_video_obj['full_path'] if first_video_obj else ""
    first_video_title = first_video_obj['name'] if first_video_obj else "No videos in this course"
    
    return render_template(
        "player.html",
        course=course_structure,
        first_video_path=first_video_path,
        first_video_title=first_video_title,
        progress=progress_data,
        course_name=course_name,
        lms_title=LMS_TITLE
    )

# Serve video
@app.route("/video/<path:filepath>")
def serve_video(filepath):
    """Serve video files from their absolute paths"""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        return send_from_directory(directory, filename)
    else:
        flash('Video file not found!', 'danger')
        return redirect(url_for('home'))

# Track watched
@app.route('/mark_watched', methods=['POST'])
def mark_watched():
    data = request.get_json()
    video_id = data.get('id')
    course = data.get('course')

    if video_id:
        progress_data[video_id] = True
        if course:
            progress_data[f"last:{course}"] = video_id

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2)

    return jsonify({'status': 'success'})

@app.route('/last_watched/<course>')
def last_watched(course):
    video_id = progress_data.get(f"last:{course}")
    return jsonify({'id': video_id})

@app.route('/reload_courses')
def reload_courses():
    """Endpoint to reload courses from the paths file"""
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)