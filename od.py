from flask import Flask, send_from_directory, render_template
from werkzeug.routing import PathConverter
import os

class SubpathConverter(PathConverter):
    regex = r'.+?'

app = Flask(__name__, static_url_path='')
app.url_map.converters['subpath'] = SubpathConverter

server_version = '0.1'

dirs = {
    'Movies': '/Movies2',
    'TV': '/TV2',
    'Music': '/Music2',
    'Books': '/Books'
}

dirFileCounts = {
    'Movies': 0,
    'TV': 0,
    'Music': 0,
    'Books': 0
}

def human_size(size, decimal_places=2):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

@app.route('/')
def root():
    # get number of files in dirs
    for key in dirs:
        try:
            dirFileCounts[key] = len(os.listdir(dirs[key]))
        except FileNotFoundError:
            dirFileCounts[key] = 0
    return render_template('index.html', moviecount=dirFileCounts['Movies'], tvcount=dirFileCounts['TV'], musiccount=dirFileCounts['Music'], bookcount=dirFileCounts['Books'], server_version=server_version)


@app.route('/static/<subpath:path>')
def static_proxy(path):
    print("got static " + path)
    if path in ["Movies", "TV", "Music", "Books"]:
        # list directory
        filesizes = []
        for file in os.listdir(dirs[path]):
            filesizes.append(human_size(os.path.getsize(dirs[path] + "/" + file)))
        return render_template('list.html', path=path, files=os.listdir(dirs[path]), filesizes=filesizes, server_version=server_version)
    else:
        # make sure the path is safe and isn't going anywhere but the allowed locations
        if path.startswith("Movies") or path.startswith("TV") or path.startswith("Music") or path.startswith("Books"):
            return send_from_directory('/', path)
        else:
            return f"<h1>403 Forbidden</h1><p>Project Endless Night OD server v{server_version}</p>", 403

@app.errorhandler(404)
def page_not_found(e):
    return f"<h1>404 Not Found</h1><p>Project Endless Night OD server v{server_version}</p>", 404

@app.errorhandler(500)
def internal_server_error(e):
    return f"<h1>500 Internal Server Error</h1><p>Project Endless Night OD server v{server_version}</p>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8092, debug=False)