// Do this as the first thing so that any code reading it knows the right env.
process.env.BABEL_ENV = 'production';
process.env.NODE_ENV = 'production';
process.env.ASSET_PATH = '/';

var webpack = require('webpack'),
  config = require('../webpack.config');

delete config.chromeExtensionBoilerplate;

config.mode = 'production';

webpack(config, function (err, stats) {
  if (err) {
    console.error(err.stack || err);
    if (err.details) {
      console.error(err.details);
    }
    process.exit(1);
  }

  const info = stats.toJson();

  if (stats.hasErrors()) {
    console.error('Build failed with errors:');
    info.errors.forEach((error) => console.error(error));
    process.exit(1);
  }

  if (stats.hasWarnings()) {
    console.warn('Build completed with warnings:');
    info.warnings.forEach((warning) => console.warn(warning));
  }

  console.log(stats.toString({
    colors: true,
    chunks: false,
    children: false,
    modules: false,
  }));

  console.log('Build completed successfully!');
});
