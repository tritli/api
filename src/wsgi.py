from api.trit_li import app, api, lfs, sfl, val, exp

if __name__ == '__main__':
    api.add_namespace(lfs)
    api.add_namespace(sfl)
    api.add_namespace(val)
    api.add_namespace(exp)
    app.run(debug=False, host='0.0.0.0', port='80')
