let manualCentroids = [];
let isManualSelection = false;

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('kmeans-canvas');
    canvas.addEventListener('click', onCanvasClick); // 为 canvas 添加点击事件监听器

    // 页面加载后获取初始数据
    fetchData();
});

// 初始化聚类中心的函数
function initClusters() {

    // 获取用户选择的初始化方法
    const initMethod = document.getElementById('init-method').value;
        
    // 获取用户输入的聚类数量 k
    const kValue = parseInt(document.getElementById('k-value').value, 10);
    if (isNaN(kValue) || kValue <= 0) {
        alert("Please enter a valid positive integer for number of clusters (k).");
        return;
    }
    if (initMethod === 'manual') {
       
        isManualSelection = true;
        if (manualCentroids.length !== kValue) {
            alert(`Please select exactly ${kValue} centroids., you clikc ${manualCentroids.length}`);
            return;
        }
        
        console.log('Manual Centroids:', manualCentroids);
        
        // 发送手动选择的中心点到后端
        fetch('/api/init_manual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                centroids: manualCentroids // 传递手动选择的中心点
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                alert(`Error: ${data.error}`);
            } else {
                console.log('Initialized Centroids:', data.centroids);
                //drawClusters(data.data, data.clusters); // 重新绘制数据点和聚类
                drawCentroids(data.centroids); // 绘制初始化的中心点
            }
        })
        .catch(error => console.error('Error:', error));
    } 
    else{
        isManualSelection = false; 
        manualCentroids = [];
        console.log(`Selected Initialization Method: ${initMethod}`);
        console.log(`Number of clusters (k): ${kValue}`);
        
        // 发送请求到后端，初始化聚类中心
        fetch('/api/init', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                init_method: initMethod,
                k_value: kValue  // 传递 k 值
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                alert(`Error: ${data.error}`);
            } else {
                console.log('Initialized Centroids:', data.centroids);
                drawCentroids(data.centroids);
            }
        })
        .catch(error => console.error('Error:', error))
        }
}

// 获取数据并绘制初始点
function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            drawPoints(data.data);
        });
}
function handleInitMethodChange() {
    const initMethod = document.getElementById('init-method').value;
    
    if (initMethod === 'manual') {
        isManualSelection = true; 
        manualCentroids = []; 
        alert("Manual mode activated. Please click on the canvas to select centroids.");
    } else {
        isManualSelection = false;
        manualCentroids = []; 
    }
}
function onCanvasClick(event) {
    if (!isManualSelection) return; // 如果不是手动选择模式，忽略点击事件

    // 获取 canvas 元素和点击的位置
    const canvas = document.getElementById('kmeans-canvas');
    const rect = canvas.getBoundingClientRect(); // 获取 canvas 相对窗口的位置
    const x = event.clientX - rect.left; // 获取点击的 x 坐标
    const y = event.clientY - rect.top;  // 获取点击的 y 坐标

    // 将点击位置转换为数据坐标
    const dataX = (x - 400) / 100; // 映射回数据坐标系
    const dataY = (y - 300) / 100; // 映射回数据坐标系

    // 检查选择的质心数量是否已经足够
    const kValue = parseInt(document.getElementById('k-value').value, 10);
    if (manualCentroids.length >= kValue) {
        alert(`You have already selected ${kValue} centroids.`);
        return;
    }

    // 将选择的点添加到手动选择的中心点数组中
    manualCentroids.push([dataX, dataY]);
    drawManualCentroids(); 

    // 更新提示信息
    const remainingK = document.getElementById('remaining-k');
    remainingK.textContent = kValue - manualCentroids.length;

    if (manualCentroids.length >= kValue) {
        isManualSelection = false;
        alert("You have selected enough centroids. Now you can initialize clusters.");
    }
}

function drawManualCentroids() {
    const canvas = document.getElementById('kmeans-canvas');
    const ctx = canvas.getContext('2d');
    
    // 绘制手动选择的中心点
    ctx.fillStyle = 'red';
    manualCentroids.forEach(point => {
        ctx.beginPath();
        ctx.arc(point[0] * 100 + 400, point[1] * 100 + 300, 7, 0, Math.PI * 2);
        ctx.fill();
    });
}

// 进行下一步
function nextStep() {
    fetch('/api/step', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            alert(`Error: ${data.error}`);
        } else {
            console.log('Next Step Centroids:', data.centroids);
            drawClusters(data.data, data.clusters); 
            drawCentroids(data.centroids);
        }
    })
    .catch(error => console.error('Error:', error));
}

// 生成新数据
function generateNewData() {
    fetch('/api/new_data')
        .then(response => response.json())
        .then(data => {
            manualCentroids = []; 
            drawPoints(data.data);
        });
}

// 直接到达收敛状态
function converge() {
    fetch('/api/converge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            alert(`Error: ${data.error}`);
        } else {
            console.log('Converged Centroids:', data.centroids);
            drawClusters(data.data, data.clusters); 
            drawCentroids(data.centroids);
        }
    })
    .catch(error => console.error('Error:', error));
}

// 绘制数据点
function drawPoints(data) {
    const canvas = document.getElementById('kmeans-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'blue';

    data.forEach(point => {
        ctx.beginPath();
        ctx.arc(point[0] * 100 + 400, point[1] * 100 + 300, 5, 0, Math.PI * 2);
        ctx.fill();
    });
}
function drawClusters(data, clusters) {
    const canvas = document.getElementById('kmeans-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const colors = [
        'blue', 'green',  'purple', 'orange', 
        'brown', 'pink', 'yellow', 'cyan', 'magenta'
    ];
    if (data.length !== clusters.length) {
        console.error("Data length and cluster length do not match!");
        return;
    }
    for (let i = 0; i < data.length; i++) {
        const point = data[i];
        const cluster = clusters[i];
        const color = colors[cluster % colors.length];  // 根据 cluster 值选择颜色

        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(point[0] * 100 + 400, point[1] * 100 + 300, 5, 0, Math.PI * 2);
        ctx.fill();
    }
}
// 绘制聚类中心点
function drawCentroids(centroids) {
    const canvas = document.getElementById('kmeans-canvas');
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'red';

    centroids.forEach(point => {
        ctx.beginPath();
        ctx.arc(point[0] * 100 + 400, point[1] * 100 + 300, 7, 0, Math.PI * 2);
        ctx.fill();
    });
}
