import os
import re
import json
import datetime
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "WORKSPACE")
RAW_DATA_DIR = os.path.join(WORKSPACE_DIR, "raw_data")
PM_DIR = os.path.join(BASE_DIR, "PROJECT_MANAGEMENT")
GOV_DIR = os.path.join(BASE_DIR, "GOVERNANCE")
ARCHIVE_DIR = os.path.join(BASE_DIR, "ARCHIVE")
LOGS_DIR = os.path.join(BASE_DIR, "LOGS")

def get_config():
    config_path = os.path.join(PM_DIR, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "current_phase": 1,
        "current_run": 1,
        "notes_per_run": 8,
        "runs_per_phase": 8
    }

def get_active_paths():
    config = get_config()
    cycle_str = f"cycle_{config['current_phase']:02d}"
    run_str = f"run_{config['current_run']:02d}"
    
    return {
        "raw_data": RAW_DATA_DIR,
        "field_notes": os.path.join(WORKSPACE_DIR, "field_notes", cycle_str, run_str),
        "project_management": PM_DIR,
        "governance": GOV_DIR,
        "reports": os.path.join(ARCHIVE_DIR, cycle_str),
        "logs": LOGS_DIR
    }

def ensure_dirs():
    paths = get_active_paths()
    for name, path in paths.items():
        os.makedirs(path, exist_ok=True)

def run_git_command(args):
    try:
        result = subprocess.run(['git'] + args, cwd=BASE_DIR, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def init_git():
    # Check if in a git repo
    success, _, _ = run_git_command(['rev-parse', '--is-inside-work-tree'])
    if not success:
        print("Git repository not detected. Initializing...")
        run_git_command(['init'])
        # Add initial configuration or files
        run_git_command(['add', '.'])
        run_git_command(['commit', '-m', 'chore: initialize agent research workspace'])
        print("Git initialized and initial commit created.")

def slugify(value):
    # Simple slugify
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

class IntakeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default logs in terminal to keep it clean, or redirect to logs
        pass

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/" or path == "/index.html":
            self.serve_static("index.html", "text/html")
        elif path == "/board" or path == "/board.html":
            self.serve_static("board.html", "text/html")
        elif path == "/api/stats":
            self.handle_stats()
        elif path == "/api/recent":
            self.handle_recent()
        elif path == "/api/report":
            self.handle_report_get(parsed_path.query)
        elif path == "/api/board":
            self.handle_board()
        elif path == "/api/matrix":
            self.handle_matrix()
        elif path == "/api/queue":
            self.handle_queue_get()
        elif path == "/api/android/status":
            self.handle_android_status()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/save":
            self.handle_save()
        elif path == "/api/queue/add":
            self.handle_queue_add()
        else:
            self.send_error(404, "Not Found")

    def serve_static(self, filename, content_type):
        filepath = os.path.join(BASE_DIR, "SERVICES", "static", filename)
        if not os.path.exists(filepath):
            self.send_error(404, "Static file not found")
            return
        
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def handle_stats(self):
        ensure_dirs()
        
        # Count helper that works recursively
        def count_files(dir_path):
            if not os.path.exists(dir_path):
                return 0
            count = 0
            for root, dirs, files in os.walk(dir_path):
                count += len([f for f in files if not f.startswith('.')])
            return count

        config = get_config()
        stats = {
            "raw_data": count_files(RAW_DATA_DIR),
            "field_notes": count_files(os.path.join(WORKSPACE_DIR, "field_notes")),
            "project_management": count_files(PM_DIR),
            "reports": count_files(ARCHIVE_DIR),
            "current_cycle": config.get("current_phase", 1),
            "current_run": config.get("current_run", 1)
        }
        self.send_json(stats)

    def handle_recent(self):
        ensure_dirs()
        
        # Categories mapping to scan
        categories = {
            "raw_data": RAW_DATA_DIR,
            "field_notes": os.path.join(WORKSPACE_DIR, "field_notes"),
            "project_management": PM_DIR,
            "governance": GOV_DIR
        }

        all_files = []
        for cat, dir_path in categories.items():
            if not os.path.exists(dir_path):
                continue
            
            # Use os.walk to find all files recursively
            for root, dirs, files in os.walk(dir_path):
                for fname in files:
                    if fname.startswith('.'):
                        continue
                    fpath = os.path.join(root, fname)
                    stat = os.stat(fpath)
                    mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                    
                    content = ""
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                    except Exception:
                        pass
                    
                    title = fname
                    if "_" in fname:
                        parts = fname.split("_", 2)
                        if len(parts) == 3:
                            title = parts[2].replace(".md", "").replace(".txt", "").replace("-", " ").title()

                    all_files.append({
                        "filename": fname,
                        "title": title,
                        "category": cat,
                        "time": mod_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "mtime": stat.st_mtime,
                        "content": content
                    })

        # Sort by mtime descending
        all_files.sort(key=lambda x: x["mtime"], reverse=True)
        self.send_json(all_files[:10])

    def handle_report_get(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        rel_path = params.get("path", [None])[0]
        if not rel_path:
            self.send_json({"error": "Path parameter is required"}, 400)
            return
        
        # Sanitize path to prevent directory traversal
        safe_path = os.path.normpath(os.path.join(BASE_DIR, rel_path))
        if not safe_path.startswith(BASE_DIR):
            self.send_json({"error": "Access denied"}, 403)
            return
        
        if not os.path.exists(safe_path) or not os.path.isfile(safe_path):
            self.send_json({"error": "File not found"}, 404)
            return
        
        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_json({"content": content})
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def handle_save(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": "Invalid JSON: " + str(e)}, 400)
            return

        title = payload.get("title", "").strip()
        content = payload.get("content", "").strip()
        category = payload.get("category", "raw_data").strip()

        if not title or not content:
            self.send_json({"error": "Title and Content are required fields."}, 400)
            return

        # Map category to directory dynamically
        paths = get_active_paths()
        target_dir = paths.get(category)
        if not target_dir:
            self.send_json({"error": f"Invalid category: {category}"}, 400)
            return

        ensure_dirs()

        # Format filename: YYYY-MM-DD_HHMMSS_slugified-title.md
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H%M%S")
        slug = slugify(title)
        filename = f"{timestamp}_{slug}.md"
        filepath = os.path.join(target_dir, filename)

        # Write to file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"> Ingested on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"> Category: {category}\n\n")
                f.write(content)
        except Exception as e:
            self.send_json({"error": f"Failed to write file: {str(e)}"}, 500)
            return

        # Perform Git commit
        rel_path = os.path.relpath(filepath, BASE_DIR)
        run_git_command(['add', rel_path])
        commit_msg = f"ingest({category}): add {title}"
        success, stdout, stderr = run_git_command(['commit', '-m', commit_msg])

        response_payload = {
            "success": True,
            "filepath": rel_path,
            "git_committed": success,
            "git_output": stdout if success else stderr
        }
        
        # Log session execution to LOGS/session_diary.md
        self.log_to_diary(commit_msg, rel_path)

        self.send_json(response_payload)

    def log_to_diary(self, action, filepath):
        diary_path = os.path.join(LOGS_DIR, "session_diary.md")
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get last git hash
        _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
        
        entry = f"## [{now_str}] Run - Commit: `{git_hash}`\n"
        entry += f"- **Action**: {action}\n"
        entry += f"- **File**: `{filepath}`\n"
        entry += f"- **Status**: Auto-committed to source of truth.\n\n"
        
        try:
            file_exists = os.path.exists(diary_path)
            with open(diary_path, "a", encoding="utf-8") as f:
                if not file_exists:
                    f.write("# Workspace Session Diary\n\n")
                f.write(entry)
        except Exception as e:
            print(f"Error updating diary: {e}")

    def handle_board(self):
        board_path = os.path.join(PM_DIR, "board_data.json")
        data = []
        if os.path.exists(board_path):
            try:
                with open(board_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass
        self.send_json(data)

    def handle_matrix(self):
        matrix_path = os.path.join(PM_DIR, "matrix_data.json")
        data = []
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass
        self.send_json(data)

    def handle_queue_get(self):
        queue_path = os.path.join(PM_DIR, "queue.json")
        data = []
        if os.path.exists(queue_path):
            try:
                with open(queue_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass
        self.send_json(data)

    def handle_queue_add(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": "Invalid JSON: " + str(e)}, 400)
            return

        task = payload.get("task", "").strip()
        if not task:
            self.send_json({"error": "Task name is required."}, 400)
            return

        queue_path = os.path.join(PM_DIR, "queue.json")
        data = []
        if os.path.exists(queue_path):
            try:
                with open(queue_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass

        new_id = max([item.get("id", 0) for item in data]) + 1 if data else 1
        new_item = {
            "id": new_id,
            "task": task,
            "status": "queued",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(new_item)

        try:
            with open(queue_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.send_json({"error": f"Failed to update queue: {str(e)}"}, 500)
            return

        self.send_json({"success": True, "task": new_item})

    def handle_android_status(self):
        # 1. Check lsusb for Vendor ID 0fce (Sony)
        lsusb_connected = False
        try:
            res = subprocess.run(["lsusb"], capture_output=True, text=True)
            if "0fce:" in res.stdout:
                lsusb_connected = True
        except Exception:
            pass

        # 2. Check adb devices
        adb_path = os.path.join(BASE_DIR, "SERVICES", "platform-tools", "adb")
        adb_connected = False
        adb_state = "offline"
        device_id = None

        if os.path.exists(adb_path):
            try:
                res_adb = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
                lines = res_adb.stdout.strip().split("\n")[1:]
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            device_id = parts[0]
                            adb_state = parts[1]
                            adb_connected = True
            except Exception:
                pass

        # 3. Classify status
        status = "offline"
        description = "Phone is unplugged or not detected on USB bus."

        if lsusb_connected:
            if adb_connected:
                if adb_state == "device":
                    status = "connected"
                    description = "Connection verified. Ready for automated browser operations."
                elif adb_state == "unauthorized":
                    status = "unauthorized"
                    description = "Please tap 'Allow USB Debugging' on the phone screen."
                elif "permission" in adb_state.lower() or "no permissions" in adb_state.lower():
                    status = "no_permissions"
                    description = "USB permissions restricted on host. Run ./SERVICES/setup_android.sh."
                else:
                    status = adb_state
                    description = f"ADB state: {adb_state}."
            else:
                status = "debugging_disabled"
                description = "Phone detected, but USB Debugging is disabled on device."

        self.send_json({
            "status": status,
            "description": description,
            "device_id": device_id,
            "lsusb_connected": lsusb_connected
        })

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server(port=8484):
    ensure_dirs()
    init_git()
    server_address = ('', port)
    httpd = HTTPServer(server_address, IntakeHandler)
    print(f"Agent Intake Server running on http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    import sys
    port = 8484
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
