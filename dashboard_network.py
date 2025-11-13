from flask import Flask, jsonify
from flask_cors import CORS
import socket
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

@app.route('/')
def home():
    local_ip = get_local_ip()
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Optimal Execution Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                line-height: 1.6;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            header {{
                background: rgba(255, 255, 255, 0.95);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                margin-bottom: 2rem;
                text-align: center;
            }}
            
            h1 {{
                color: #2c3e50;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
            }}
            
            .network-info {{
                background: #2c3e50;
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
                font-family: 'Courier New', monospace;
            }}
            
            .dashboard-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 2rem;
            }}
            
            .card {{
                background: rgba(255, 255, 255, 0.95);
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            
            .card h2 {{
                color: #2c3e50;
                margin-bottom: 1rem;
                font-size: 1.4rem;
                border-bottom: 2px solid #3498db;
                padding-bottom: 0.5rem;
            }}
            
            .control-group {{
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin: 1.5rem 0;
                flex-wrap: wrap;
            }}
            
            .control-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            
            label {{
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #2c3e50;
            }}
            
            input, select {{
                padding: 0.8rem 1rem;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 1rem;
            }}
            
            button {{
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                margin: 0.5rem;
            }}
            
            .metric {{
                display: flex;
                justify-content: space-between;
                margin: 0.5rem 0;
                padding: 0.5rem;
                background: rgba(52, 152, 219, 0.1);
                border-radius: 5px;
            }}
            
            .metric-value {{
                font-weight: 600;
                color: #2980b9;
            }}
            
            .success {{
                color: #27ae60;
                background: #d5f4e6;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            
            .error {{
                color: #e74c3c;
                background: #fadbd8;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🎯 Optimal Execution Dashboard</h1>
                <p>Network Access Enabled - Accessible from any device on your network</p>
                
                <div class="network-info">
                    <div><strong>Local Access:</strong> http://localhost:5001</div>
                    <div><strong>Network Access:</strong> http://{local_ip}:5001</div>
                    <div><strong>Your Current IP:</strong> {request.remote_addr if 'request' in locals() else 'Unknown'}</div>
                </div>
            </header>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h2>🚀 Quick Execution</h2>
                    <div class="control-group">
                        <div class="control-item">
                            <label for="orderSize">Order Size</label>
                            <input type="number" id="orderSize" value="100000">
                        </div>
                        <div class="control-item">
                            <label for="urgency">Urgency</label>
                            <input type="range" id="urgency" min="0" max="1" step="0.1" value="0.5">
                            <span id="urgencyValue">0.5</span>
                        </div>
                    </div>
                    <button onclick="executeOrder()">Execute Order</button>
                    <div id="executionResult"></div>
                </div>
                
                <div class="card">
                    <h2>📊 Market Data</h2>
                    <button onclick="loadMarketData()">Load Market Conditions</button>
                    <div id="marketData"></div>
                </div>
                
                <div class="card">
                    <h2>🔍 Liquidity Analysis</h2>
                    <button onclick="loadLiquidityData()">Analyze Liquidity</button>
                    <div id="liquidityData"></div>
                </div>
                
                <div class="card">
                    <h2>⚡ System Status</h2>
                    <div class="metric">
                        <span>Server Status:</span>
                        <span class="metric-value" style="color: #27ae60;">✅ Online</span>
                    </div>
                    <div class="metric">
                        <span>Network Access:</span>
                        <span class="metric-value" style="color: #27ae60;">✅ Enabled</span>
                    </div>
                    <div class="metric">
                        <span>CORS Support:</span>
                        <span class="metric-value" style="color: #27ae60;">✅ Active</span>
                    </div>
                    <div class="metric">
                        <span>Your IP:</span>
                        <span class="metric-value">{request.remote_addr if 'request' in locals() else 'Unknown'}</span>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Update urgency display
            document.getElementById('urgency').addEventListener('input', function() {{
                document.getElementById('urgencyValue').textContent = this.value;
            }});

            async function executeOrder() {{
                const orderSize = document.getElementById('orderSize').value;
                const urgency = document.getElementById('urgency').value;
                
                const resultDiv = document.getElementById('executionResult');
                resultDiv.innerHTML = '<div class="success">🔄 Executing order...</div>';
                
                try {{
                    const response = await fetch('/api/execute', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            order_size: parseInt(orderSize),
                            urgency: parseFloat(urgency)
                        }})
                    }});
                    
                    const data = await response.json();
                    resultDiv.innerHTML = `<div class="success">✅ ${{data.message}}</div>`;
                }} catch (error) {{
                    resultDiv.innerHTML = `<div class="error">❌ Error: ${{error.message}}</div>`;
                }}
            }}

            async function loadMarketData() {{
                const marketDiv = document.getElementById('marketData');
                marketDiv.innerHTML = '<div class="success">📊 Loading market data...</div>';
                
                try {{
                    const response = await fetch('/api/analysis');
                    const data = await response.json();
                    
                    marketDiv.innerHTML = `
                        <div class="success">✅ Market Data Loaded</div>
                        <div class="metric">
                            <span>Volatility:</span>
                            <span class="metric-value">${{(data.market_conditions.volatility * 100).toFixed(2)}}%</span>
                        </div>
                        <div class="metric">
                            <span>Volume:</span>
                            <span class="metric-value">${{data.market_conditions.average_volume.toLocaleString()}}</span>
                        </div>
                        <div class="metric">
                            <span>Momentum:</span>
                            <span class="metric-value">${{(data.market_conditions.momentum * 100).toFixed(2)}}%</span>
                        </div>
                    `;
                }} catch (error) {{
                    marketDiv.innerHTML = `<div class="error">❌ Error loading data</div>`;
                }}
            }}

            async function loadLiquidityData() {{
                const liquidityDiv = document.getElementById('liquidityData');
                liquidityDiv.innerHTML = '<div class="success">🔍 Analyzing liquidity...</div>';
                
                try {{
                    const response = await fetch('/api/analysis');
                    const data = await response.json();
                    
                    let liquidityHTML = '<div class="success">✅ Liquidity Analysis Complete</div>';
                    
                    if (data.hidden_liquidity) {{
                        if (data.hidden_liquidity.hidden_buy_pressure) {{
                            liquidityHTML += `<div class="metric">
                                <span>Buy Pressure:</span>
                                <span class="metric-value">${{(data.hidden_liquidity.hidden_buy_pressure * 100).toFixed(1)}}%</span>
                            </div>`;
                        }}
                        if (data.hidden_liquidity.hidden_sell_pressure) {{
                            liquidityHTML += `<div class="metric">
                                <span>Sell Pressure:</span>
                                <span class="metric-value">${{(data.hidden_liquidity.hidden_sell_pressure * 100).toFixed(1)}}%</span>
                            </div>`;
                        }}
                        if (data.hidden_liquidity.iceberg_indication) {{
                            liquidityHTML += `<div class="metric">
                                <span>Iceberg Orders:</span>
                                <span class="metric-value">${{(data.hidden_liquidity.iceberg_indication * 100).toFixed(1)}}%</span>
                            </div>`;
                        }}
                    }}
                    
                    liquidityDiv.innerHTML = liquidityHTML;
                }} catch (error) {{
                    liquidityDiv.innerHTML = `<div class="error">❌ Error loading liquidity data</div>`;
                }}
            }}

            // Test connection on load
            window.addEventListener('load', async () => {{
                console.log('🌐 Network Dashboard Loaded');
                try {{
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    console.log('✅ Server health:', data);
                }} catch (error) {{
                    console.log('❌ Server connection failed:', error);
                }}
            }});
        </script>
    </body>
    </html>
    '''

@app.route('/api/execute', methods=['POST'])
def api_execute():
    data = request.json
    return jsonify({
        'status': 'success',
        'message': f'Order for {data.get("order_size", 0):,} shares executed successfully!',
        'order_size': data.get('order_size', 0),
        'estimated_cost': data.get('order_size', 0) * 0.008
    })

@app.route('/api/analysis')
def api_analysis():
    return jsonify({
        'market_conditions': {
            'volatility': 0.023,
            'average_volume': 1500000,
            'momentum': 0.008,
            'spread': 0.012
        },
        'hidden_liquidity': {
            'hidden_buy_pressure': 0.25,
            'hidden_sell_pressure': 0.35,
            'iceberg_indication': 0.15
        }
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'healthy',
        'service': 'optimal_execution',
        'network': 'enabled',
        'client_ip': request.remote_addr
    })

if __name__ == '__main__':
    local_ip = get_local_ip()
    
    print("🚀 NETWORK-ENABLED OPTIMAL EXECUTION DASHBOARD")
    print("=" * 50)
    print(f"📱 Local Access:    http://localhost:5001")
    print(f"🌐 Network Access:  http://{local_ip}:5001")
    print(f"📡 Your IP:         {local_ip}")
    print(f"👤 Client IP:       Will show when connected")
    print("=" * 50)
    print("🔧 Features:")
    print("   ✅ CORS Enabled")
    print("   ✅ Network Access")
    print("   ✅ Real-time Execution")
    print("   ✅ Market Analysis")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
    except Exception as e:
        print(f"❌ Failed to start: {e}")