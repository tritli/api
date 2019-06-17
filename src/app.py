from api.trit_li import app, api, lfs, sfl, val

if __name__ == '__main__':
    api.add_namespace(lfs)
    api.add_namespace(sfl)
    api.add_namespace(val)
    app.run(debug=False, host='0.0.0.0', port='20202')
