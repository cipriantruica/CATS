__author__ = "Adrien Guille"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "adrien.guille@univ-lyon2.fr"
__status__ = "Production"

from flask import Flask, Response, render_template, request
from indexing.vocabulary_index import VocabularyIndex
from search_mongo import Search
import pymongo
from nlplib.lemmatize_text import LemmatizeText

# Connecting to the database
client = pymongo.MongoClient()
dbname = 'TwitterDB2'
db = client[dbname]

app = Flask(__name__)

query = {}

def getTweetCount(query = {}):
    #print query
    return db.documents.find(query).count()

@app.route('/cats/analysis')
def analysis_dashboard_page(name=None):
    tweetCount = getTweetCount()
    return render_template('analysis.html', name=name, tweetCount=tweetCount) 

@app.route('/cats/analysis', methods=['POST'])
def analysis_dashboard_page2():
    keywords = request.form['keyword']
    date = request.form['date']
    lem = LemmatizeText(keywords)
    lem.createLemmaText()
    lem.createLemmas()
    wordList = []
    for word in lem.wordList:
    	wordList.append(word.word)
    global query
    query = {"words.word" : {"$in": wordList }, "date": {"$gt": "2015-04-10", "$lte":  "2015-04-12"}}
    tweetCount = getTweetCount(query)
    return render_template('analysis.html', tweetCount=tweetCount)  
    
@app.route('/cats/about')
def about_page(name=None):
    return render_template('about.html', name=name)    

@app.route('/cats/analysis/construct_vocabulary')
def construct_vocabulary():
    print("constructing vocab")	
    vocab = VocabularyIndex(dbname)
    vocab.createIndex()
    return analysis_dashboard_page()

@app.route('/cats/analysis/vocabulary_cloud')
def getTermCloud():
    
    voc = db.vocabulary.find(projection={'word':1,'idf':1},limit=250).sort('idf',pymongo.ASCENDING)
    html = """
    <!doctype html>
    <!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"><![endif]-->
    <!--[if IE 7]><html class="no-js lt-ie9 lt-ie8" lang="en"><![endif]-->
    <!--[if IE 8]><html class="no-js lt-ie9" lang="en"><![endif]-->
    <!--[if gt IE 8]><!-->
    <html class="no-js" lang="en">
    <!--<![endif]-->
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script src="/static/jquery-1.11.1.min.js"></script>
    <script src="/static/jquery.awesomeCloud-0.2.js"></script>
    <style type="text/css">
    .wordcloud {
    border: 1px solid #036;
    height: 7in;
    margin: 0.5in auto;
    padding: 0;
    page-break-after: always;
    page-break-inside: avoid;
    width: 7in;
    }
    </style>
    </head>
    <body>
    <div role="main">
    <div id="wordcloud2" class="wordcloud">
    """
    for doc in voc :
        weight = round((1/doc['idf'])*333)
        html += "<span data-weight='"+str(weight)+"'>"+doc['word']+"</span>\n"
    html += """</div>
            <script>
    			$(document).ready(function(){
    				$("#wordcloud2").awesomeCloud({
    					"size" : {
    						"grid" : 20,
    						"factor" : 0.25
    					},
    					"options" : {
    						"color" : "random-dark",
    						"rotationRatio" : 0.35
    					},
    					"font" : "'Times New Roman', Times, serif",
    					"shape" : "circle"
    				});
    			});
    		</script>
        </body>
    </html>
    """
    return html

@app.route('/cats/analysis/vocabulary.csv')
def getTerms():
    print 'ok', query
    if query:
        vocab = VocabularyIndex(dbname)
        vocab.createIndex(query)
        voc = db.vocabulary_query.find(projection={'word':1,'idf':1},limit=1000).sort('idf',pymongo.ASCENDING)
    else:
        voc = db.vocabulary.find(projection={'word':1,'idf':1},limit=1000).sort('idf',pymongo.ASCENDING)
    csv = 'word,idf\n'
    for doc in voc :
        csv += doc['word']+','+str(doc['idf'])+'\n'
    return Response(csv,mimetype="text/csv")   

@app.route('/cats/analysis/tweets',methods=['POST'])
def getTweets():
    query = request.form['cooccurringwords']
    search = Search(searchPhrase=query,dbname=dbname)
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