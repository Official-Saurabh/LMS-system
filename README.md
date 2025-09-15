# Saurabh's LMS

A modern, self-hosted Learning Management System built with Flask for organizing and watching video courses with progress tracking.

## Quick Start

### Installation

1. Install Flask:
```bash
pip install Flask==3.0.0
```

2. Configure Your Courses

Edit the `course_paths.txt` file to add your course directories:
```
Course Name = /path/to/your/course/folder
```

Example:
```
Python Basics = C:\Courses\Python-Basics
Web Development = /home/user/courses/web-dev
Docker Course = D:\Docker\courses\Docker-Basics
```

3. Run the application:
```bash
python run.py
```

The LMS will start on `http://127.0.0.1:5000` and open in your browser.

## Configuration

### Authentication (Optional)
Edit `config.json` to set up login credentials:
```json
{
  "lms_title": "Your LMS Name",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  }
}
```
Leave credentials empty to disable authentication.

## Keyboard Shortcuts

- **Space/K**: Play/Pause
- **←/→**: Rewind/Fast forward 10s
- **↑/↓**: Volume up/down
- **F**: Toggle fullscreen
- **M**: Mute/Unmute
- **Ctrl+B**: Toggle sidebar
- **Ctrl+T**: Toggle theme

## Supported Formats

MP4, MKV, AVI, MOV, M4V, WebM, FLV, WMV, MPEG

## Troubleshooting

- **Port 5000 in use**: Change port in `run.py`
- **Course not found**: Check paths in `course_paths.txt`
- **Videos not playing**: Verify format support and file permissions

---

**Happy learning! 🚀**
