from flask import Flask, render_template, jsonify, request, send_file
import os
from logger import logging, loggerInit
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import config as conf

if not os.path.exists(conf.files_dir):
    os.mkdir(conf.files_dir)

loggerInit('app.log')

app = Flask(__name__)

def default_response():
    return jsonify({'status': 'ok'})

def default_error():
    return jsonify({'status': 'error'})

@app.route('/')
def default_route():
    return render_template("index.html")

@app.post('/files/xyu')
async def xyu():
    return jsonify({'xyu': 'xyu', 'abc':'abc'})

@app.get('/files')
async def get_files():
    return jsonify([{ 'path': f'{conf.files_url}{i}', 'filename': i } for i in os.listdir(conf.files_dir)])

@app.post('/files')
async def upload_file():
    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(conf.files_dir, f.filename))
    return default_response()


@app.get('/files/<filename>')
async def get_file(filename):
    filepath = os.path.join(conf.files_dir, filename)
    try:
        return send_file(filepath)
    except FileNotFoundError as e:
        logging.info(f'Requested file does not exists. PATH: {filepath}')
        return default_error(), 404

@app.delete('/files/<filename>')
async def delete_file(filename):
    filepath = os.path.join(conf.files_dir, filename)
    try:
        os.remove(filepath)
        return default_response()
    except FileNotFoundError as e:
        logging.error(f'Requested file does not exists. PATH: {filepath}')
        return default_response(), 404

async def main():
    await serve(WsgiToAsgi(app), Config().from_pyfile('config.py'))

if __name__ == '__main__':
    asyncio.run(main())
