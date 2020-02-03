from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# '/' 주소로 들어갔을 때 'This is Home!' 을 보여줌
## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분
@app.route('/new', methods=['POST'])
def new_post():
   rank_receive = int(request.form['rank_give'])
   star_receive = request.form['star_give']
   title_receive = request.form['title_give']

   db.movies.insert_one({'rank': rank_receive, 'star': star_receive, 'title': title_receive})

   return jsonify({'result': 'success'})

@app.route('/test', methods=['GET'])
def test_get():
   rank_receive = request.args.get('rank_give')   # rank_give로 클라이언트가 준 rank를 가져오기
   rank_receive = int(rank_receive)               # rank_receive를 숫자로 만들어주기
                                                  # ^ db엔 숫자로 저장되어있으니까

   # rank의 값이 받은 rank와 일치하는 document 찾기 & _id 값은 출력에서 제외하기{'_id':0}
   movie_info = db.movies.find_one({'rank':rank_receive},{'_id':0})

   # info라는 키 값으로 영화정보로 내려주기
   return jsonify({'result':'success', 'info':movie_info})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
