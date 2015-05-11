from flask import Flask, Response, render_template, request
from indexing.vocabulary_index import VocabularyIndex
from search_mongo import Search
import pymongo

client = pymongo.MongoClient()
db = client['TwitterDB']

app = Flask(__name__)

def getTweetCount():
   tweetCount = db.documents.count()
   return tweetCount

@app.route('/cats/analysis')
def analysis_dashboard_page(name=None):
    tweetCount = getTweetCount()
    return render_template('analysis.html', name=name, tweetCount=tweetCount)  
    
@app.route('/cats/about')
def about_page(name=None):
    return render_template('about.html', name=name)    

@app.route('/cats/analysis/construct_vocabulary')
def construct_vocabulary():
    print("constructing voxcab")
    vocab = VocabularyIndex(dbname='TwitterDB')
    vocab.createIndex()

@app.route('/cats/analysis/vocabulary_cloud')
def getTermCloud():
    voc = db.vocabulary.find(projection={'word':1,'idf':1},limit=1000).sort('idf',pymongo.ASCENDING)
    csv = 'word,idf\n'
    for doc in voc :
        csv += doc['word']+','+str(doc['idf'])+'\n'
    return Response(csv,mimetype="text/csv")

@app.route('/cats/analysis/vocabulary.csv')
def getTerms():
    voc = db.vocabulary.find(projection={'word':1,'idf':1},limit=1000).sort('idf',pymongo.ASCENDING)
    csv = 'word,idf\n'
    for doc in voc :

        csv += doc['word']+','+str(doc['idf'])+'\n'
    return Response(csv,mimetype="text/csv")

@app.route('/cats/analysis/tweets',methods=['POST'])
def getTweets():
    query = request.form['cooccurringwords']
    search = Search(query)
    results = search.results()
    csv = 'author,timestamp,text,score\n'
    html = """  
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/jquery.dataTables.css">
        <style type="text/css" class="init"></style>
        <script type="text/javascript" language="javascript" src="/static/jquery-1.11.1.min.js"></script>
    	<script type="text/javascript" language="javascript" src="/static/jquery.dataTables.min.js"></script>
        <script type="text/javascript" class="init">
            $(document).ready(function() {
    	        $('#example').DataTable();
            } );
        </script>
    </head>
    <body>
        <table id="example" class="display" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th>Author</th>
                    <th>Timestamp</th>
                    <th>Text</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
    """
    for doc in results :
        html += "<tr><td>"+str(doc['author'])+'</td><td>'+str(doc['date'])+'</td><td>'+doc['rawText']+'</td><td>'+str(doc['score'])+'</td></tr>'
        csv += str(doc['author'])+','+str(doc['date'])+','+doc['rawText']+','+str(doc['score'])+'\n'
    html += "</tbody></table></body></html>"
    return html
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
