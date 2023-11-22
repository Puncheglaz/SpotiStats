#!/bin/env python3

from flask import Flask, request, send_from_directory, render_template
import pyodbc
import traceback
import detail.init
import detail.page.catalogue
import detail.page.login
import detail.page.register
import detail.page.logout
import detail.page.settings
import detail.page.myborrows
import detail.page.users
import detail.page.overdue
import detail.page.author
import detail.page.publisher
import detail.page.book
import detail.api.search_users
import detail.page.addbook

app = Flask(__name__)

conn = detail.init.init()

def error_handler(func):
    def Inner_Function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # print(e)
            traceback.print_exc()
            return render_template('pages/error.html', code = 500)
    Inner_Function.__name__ = func.__name__
    return Inner_Function


@app.route('/')
@error_handler
def page_index():
    return detail.page.catalogue.render(conn, request)


@app.route('/login', methods=['GET', 'POST'])
@error_handler
def page_login():
    return detail.page.login.render(conn, request)


@app.route('/register', methods=['GET', 'POST'])
@error_handler
def page_register():
    return detail.page.register.render(conn, request)


@app.route('/assets/<path:path>')
@error_handler
def page_assets(path):
  return send_from_directory('assets', path)


@app.route('/logout')
@error_handler
def page_logout():
    return detail.page.logout.render(conn, request)


@app.route('/settings', methods=['GET', 'POST'])
@error_handler
def page_settings():
    return detail.page.settings.render(conn, request)


@app.route('/myborrows')
@error_handler
def page_myborrows():
    return detail.page.myborrows.render(conn, request)


@app.route('/addlibr', methods=['GET', 'POST'])
@error_handler
def page_addlibr():
    return detail.page.register.render(conn, request, is_user = False)


@app.route('/users')
@error_handler
def page_users():
    return detail.page.users.render(conn, request)


@app.route('/overdue', methods=['GET', 'POST'])
@error_handler
def page_overdue():
    return detail.page.overdue.render(conn, request)


@app.route('/author/<id>', methods=['GET', 'POST'])
@error_handler
def page_author(id):
    return detail.page.author.render(conn, request, id)


@app.route('/publisher/<id>', methods=['GET', 'POST'])
@error_handler
def page_publisher(id):
    return detail.page.publisher.render(conn, request, id)


@app.route('/book/<id>', methods=['GET', 'POST'])
@error_handler
def page_book(id):
    return detail.page.book.render(conn, request, id)


@app.route('/api/search_users', methods=['POST'])
@error_handler
def api_search_users():
    return detail.api.search_users.render(conn, request)


@app.route('/addbook', methods=['GET', 'POST'])
@error_handler
def page_addbook():
    return detail.page.addbook.render(conn, request)


if __name__ == '__main__':
    app.run(debug = True)

# conn.close()
print('finished')