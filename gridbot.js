const url = "wss://stream.binance.com:9443/ws/btcusdt@ticker";
const socket = new WebSocket(url);
api_key = '2HnmgAWGh2pBvEEnhaDXwYanyc4FJRbjwV2VlPrXD9XeW7xWx1voT8T3wzoVK1On'
api_secret = 'iHi4UbGOYRO0gxK6kYzjCojnJRUXdNqfIZaZn8Pu978IbEAR6F5krMMZYVR5Jon1'
const tradesElement = document.getElementById('trades');
const quotesElement = document.getElementById('quotes'); 

var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 580,
    height: 620,
	layout: {
		backgroundColor: '#161a1e',
		textColor: '#ffffff',
	},
	grid: {
		vertLines: {
			color: '#404040',
		},
		horzLines: {
			color: '#404040',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: '#cccccc',
	},
	timeScale: {
		borderColor: '#cccccc',
		timeVisible: true,
	},
});
var candleSeries = chart.addCandlestickSeries();
var start = new Date(Date.now() - (7200 * 1000)).toISOString();
var bars_url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h"

let currentBar = {};
let trades = [];
fetch(bars_url).then((r) => r.json())
.then((response) => {
    // console.log(response);
    
    const data = response.map(bar => (
        {
            open: bar[1],
            high: bar[2],
            low: bar[3],
            close: bar[4],
            time: bar[0]/1000
        }
    ));

    currentBar = data[data.length-1];

    // console.log(data);

    candleSeries.setData(data);

})

socket.onmessage = function(event){
    const data = JSON.parse(event.data)
    // console.log(data);
    
    const tradeElement = document.createElement('div');
    tradeElement.className = 'trades';
    tradeElement.innerHTML = `<b>${data.E}</b> ${data.c} ${data.Q}`;
    tradesElement.appendChild(tradeElement);
    var elements = document.getElementsByClassName('trades');
    if(elements.length>5){
        tradesElement.removeChild(elements[0]);
    }


    //quotes
    const quoteElement = document.createElement('div');
    quoteElement.className = 'quotes';
    quoteElement.innerHTML = `<b>${data.a}</b> ${data.b}`;
    quotesElement.appendChild(quoteElement);
    var elements_quotes = document.getElementsByClassName('quotes');
    if(elements_quotes.length>10){
        quotesElement.removeChild(elements_quotes[0]);
    }

    trades.push(data.c);
            var open = trades[0];
            var high = Math.max(...trades);
            var low = Math.min(...trades);
            var close = trades[trades.length - 1];
            // console.log(open, high, low, close);

            candleSeries.update({
                time: currentBar.time + 60,
                open: open,
                high: high,
                low: low,
                close: close
            })
}

const orderSocket = new WebSocket("ws://localhost:9001");

orderSocket.onopen = function(data) {
    //orderSocket.send('ui');
}
const opensElement = document.getElementById('open_orders');
const closesElement = document.getElementById('closed_orders');
orderSocket.onmessage = function(event) {
    console.log('received message from server');
    console.log(event.data);
    if(event.data!="Hey all, a new client has joined us"){
        if(event.data[1]=='s'){
            const closeElement = document.createElement('div');
            closeElement.className = 'closed_orders';
            closeElement.innerHTML = `<b>${event.data}</b>`;
            closesElement.appendChild(closeElement);
            var opelements = document.getElementsByClassName('closed_orders');
            if(opelements.length>10){
                closesElement.removeChild(opelements[0]);
            }
        }else{
    const openElement = document.createElement('div');
    openElement.className = 'open_orders';
    openElement.innerHTML = `<b>${event.data}</b>`;
    opensElement.appendChild(openElement);
    var opelements = document.getElementsByClassName('open_orders');
    if(opelements.length>10){
        opensElement.removeChild(opelements[0]);
    }
}
}
}
