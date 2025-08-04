# Saurabh's LMS - Learning Management System

A modern, self-hosted Learning Management System (LMS) built with Flask that allows you to organize and watch your video courses with progress tracking and a beautiful, responsive interface.

## Features

- 🎥 **Video Player**: Advanced video player with keyboard shortcuts and progress tracking
- 📚 **Course Management**: Organize courses in folders with automatic discovery
- 📊 **Progress Tracking**: Track your learning progress across all courses
- 🎨 **Modern UI**: Beautiful, responsive design with dark/light theme support
- 🔐 **Authentication**: Optional login system for security
- ⌨️ **Keyboard Shortcuts**: Quick navigation and video controls
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Dependencies

### Python Dependencies

The following Python packages are required to run the LMS:

```bash
Flask==3.0.0
```

### External Libraries (CDN)

The following libraries are loaded from CDN and don't require local installation:

- **Video.js** (v8.5.2) - Advanced HTML5 video player
- **Video.js Seek Buttons Plugin** - Additional video controls
- **Font Awesome** (v6.4.0) - Icon library
- **Google Fonts (Inter)** - Modern typography

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

Download the project files to your local machine.

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install Flask==3.0.0
```

### Step 3: Configure Your Courses

1. Edit the `course_paths.txt` file to add your course directories:
   ```
   Course Name = /path/to/your/course/folder
   ```

   Example:
   ```
   Python Basics = C:\Courses\Python-Basics
   Web Development = /home/user/courses/web-dev
   Docker Course = D:\Docker\courses\Docker-Basics
   ```

2. (Optional) Configure authentication in `config.json`:
   ```json
   {
     "lms_title": "Your LMS Name",
     "credentials": {
       "username": "your_username",
       "password": "your_password"
     }
   }
   ```
   
   Leave username and password empty to disable authentication.

### Step 4: Run the Application

```bash
python run.py
```

The application will start on `http://127.0.0.1:5000` and automatically open in your default browser.

## Usage Guide

### Getting Started

1. **Access the LMS**: Open your browser and go to `http://127.0.0.1:5000`
2. **Login** (if configured): Enter your credentials if authentication is enabled
3. **Browse Courses**: View all available courses on the homepage
4. **Select a Course**: Click on any course card to start learning

### Video Player Features

#### Keyboard Shortcuts

- **Space/K**: Play/Pause video
- **Left Arrow**: Rewind 10 seconds
- **Right Arrow**: Fast forward 10 seconds
- **Up Arrow**: Increase volume
- **Down Arrow**: Decrease volume
- **F**: Toggle fullscreen
- **M**: Mute/Unmute
- **Ctrl+B**: Toggle sidebar
- **Ctrl+T**: Toggle theme
- **Ctrl+E**: Expand/Collapse all folders

#### Video Controls

- **Progress Bar**: Click to jump to specific time
- **Volume Control**: Adjust volume with slider
- **Playback Speed**: Change video speed
- **Seek Buttons**: Quick 10-second jumps forward/backward

### Course Navigation

#### Sidebar Features

- **Course Structure**: Hierarchical view of all videos and folders
- **Progress Indicators**: Visual indicators for watched videos
- **Quick Navigation**: Click any video to start playing
- **Folder Expansion**: Expand/collapse folders to organize content

#### Progress Tracking

- **Automatic Tracking**: Progress is saved automatically as you watch
- **Visual Indicators**: Watched videos show checkmarks
- **Progress Percentage**: See completion percentage for each course
- **Resume Feature**: Automatically resume from last watched video

### Theme and Customization

- **Dark/Light Theme**: Toggle between themes using the theme button
- **Responsive Design**: Interface adapts to different screen sizes
- **Modern UI**: Glassmorphism design with smooth animations

## File Structure

```
├── app/
│   ├── __init__.py          # Main Flask application
│   └── templates/
│       ├── index.html       # Homepage template
│       ├── player.html      # Video player template
│       └── login.html       # Login page template
├── config.json              # LMS configuration
├── course_paths.txt         # Course directory paths
├── progress.json            # User progress data (auto-generated)
├── run.py                   # Application entry point
└── README.md               # This file
```

## Configuration

### config.json

```json
{
  "lms_title": "Your LMS Name",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

### course_paths.txt

```
# Course Paths Configuration
# Add your course paths below, one per line
# Format: Course Name = /path/to/course/directory

Python Basics = C:\Courses\Python-Basics
Web Development = /home/user/courses/web-dev
Docker Course = D:\Docker\courses\Docker-Basics
```

## Supported Video Formats

The LMS supports the following video formats:
- MP4 (.mp4)
- MKV (.mkv)
- AVI (.avi)
- MOV (.mov)
- M4V (.m4v)
- WebM (.webm)
- FLV (.flv)
- WMV (.wmv)
- MPEG (.mpeg, .mpg)

## Troubleshooting

### Common Issues

1. **Port 5000 Already in Use**
   - Change the port in `run.py` or stop other applications using port 5000

2. **Course Not Found**
   - Check that the path in `course_paths.txt` is correct and exists
   - Ensure the directory contains video files

3. **Videos Not Playing**
   - Verify video format is supported
   - Check file permissions
   - Ensure video files are not corrupted

4. **Authentication Issues**
   - Check `config.json` configuration
   - Clear browser cookies if needed

### Performance Tips

- Use SSD storage for better video loading performance
- Organize courses in logical folder structures
- Keep video files in common formats (MP4 recommended)

## Development

### Running in Development Mode

```bash
python -c "from app import app; app.run(debug=True)"
```

### Adding New Features

The application is built with:
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Templates**: Jinja2
- **Video Player**: Video.js
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your course paths are properly configured

---

**Enjoy learning with your personalized LMS! 🚀**
