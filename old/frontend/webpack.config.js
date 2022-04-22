const path = require('path');

module.exports = {
	entry: {
		overview: './src/overview.js',
		course: './src/course.js',
		monalect: './src/monalect.js',
		home: './src/home.js',
		notebook: './src/notebook.js'
	},
	output: {
		filename: '[name].js',
		path: __dirname + '/static/'
	},
	mode: "development",
	devtool: "source-map"
}
