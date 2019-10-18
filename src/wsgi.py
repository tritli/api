from api.trit_li import app, api, lfs, sfl, val, exp
from config import HOST, PORT

if __name__ == '__main__':
    api.add_namespace(lfs)
    api.add_namespace(sfl)
    api.add_namespace(val)
    api.add_namespace(exp)
    app.run(debug=False, host=HOST, port=PORT)
