from flask import Flask, render_template, jsonify, request
import numpy as np
from kmeans import KMeans
import logging
print("Flask application is starting...") 
app = Flask(__name__)

# Initialize a global dataset
data = np.vstack((np.random.randn(50, 2) * 0.75 + np.array([1, 0]),
                  np.random.randn(50, 2) * 0.25 + np.array([-1, -1]),
                  np.random.randn(50, 2) * 0.5 + np.array([2, 2])))

kmeans = KMeans(k=3, init_method='random')
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def initialize():
    global kmeans
    init_method = request.json.get('init_method', 'random')
    k_value = request.json.get('k_value', 3)
    kmeans = KMeans(k=k_value, init_method=init_method)
    if init_method == 'mannual':
        centroids = request.json.get('centroids', [])
        if len(centroids) == 0:
            raise ValueError("No centroids provided.")
        
        kmeans.centroids = np.array(centroids)
        
        return jsonify({
            
            'centroids': kmeans.centroids.tolist()
        })
    else:
        
        centroids = kmeans.app_initialize_centroids(data).tolist()
    
   #kmeans.centroids=centroids
    return jsonify({'centroids': centroids})

@app.route('/api/step', methods=['POST'])
def step():
    global kmeans
    
    clusters = kmeans.assign_clusters(np.asarray(data))
    kmeans.centroids = kmeans.update_centroids(np.asarray(data), clusters)
    centroids = kmeans.centroids.tolist()
    clusters=[int(i) for i in clusters]
    #centroids=[[int(i[0]),int(i[1])] for i in centroids[0]]
    
    return jsonify({'centroids': centroids, 'clusters': clusters,'data':data.tolist()})
@app.route('/api/converge', methods=['POST'])
def converge():
    global kmeans
    
    centroids, clusters = kmeans.converge(np.asarray(data))
    # kmeans.centroids = kmeans.update_centroids(np.asarray(data), clusters)
    centroids = kmeans.centroids.tolist()
    clusters=[int(i) for i in clusters]
    #centroids=[[int(i[0]),int(i[1])] for i in centroids[0]]
    
    return jsonify({'centroids': centroids, 'clusters': clusters,'data':data.tolist()})

@app.route('/api/data')
def get_data():
    global data
    return jsonify({'data': data.tolist()})

@app.route('/api/new_data')
def new_data():
    global data
    data = np.vstack((np.random.randn(50, 2) * 0.75 + np.array([1, 0]),
                      np.random.randn(50, 2) * 0.25 + np.array([-1, -1]),
                      np.random.randn(50, 2) * 0.5 + np.array([2, 2])))
    return jsonify({'data': data.tolist()})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
