module.exports = {
	context: __dirname + "/eitu/static/app",
	entry: [
		'babel-polyfill',
		'./index.js'
	],
	output: {
		path: __dirname + '/eitu/static/dist',
		filename: 'bundle.js'
	},
	resolve: {
		extensions: ['', '.js', '.jsx'],
	},
	module: {
		loaders: [{
			test: /\.(js|jsx)$/,
			loader: 'babel',
		}]
	},
}

