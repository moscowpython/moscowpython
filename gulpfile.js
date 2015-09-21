var gulp = require('gulp');

var postcss = require('gulp-postcss'),
    fs = require("fs"),
    postcssImport = require("postcss-import"),
    postcssVars = require("postcss-simple-vars"),
    postcssNested = require("postcss-nested"),
    sourcemaps = require('gulp-sourcemaps'),
    autoprefixer = require('autoprefixer-core'),
    mqpacker = require('css-mqpacker'),
    csswring = require('csswring');

var imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant');

var uglify = require('gulp-uglify'),
    babel = require("gulp-babel"),
    concat = require('gulp-concat');


var lr = require('tiny-lr'),
    server = lr();

var rimraf = require('rimraf');

var browserSync = require('browser-sync'),
    reload = browserSync.reload;

var path = {
    build: { // куда складывать готовые после сборки файлы
        js: 'build/js/',
        style: 'build/css/',
        img: 'build/images/'
    },
    assets: {
        js: 'assets/js/**/*.js',
        style: 'assets/css/**/*.css',
        img: 'assets/images/**/*.*'
    },
    clean: './build'
};

gulp.task('compile:css', function () {
    var processors = [
        postcssImport(),
        postcssNested,
        postcssVars,
        autoprefixer({browsers: ['last 2 version']}),
        mqpacker,
        csswring
    ];
    return gulp.src('assets/css/*.css')
      .pipe(sourcemaps.init())
      .pipe(postcss(processors))
      .pipe(sourcemaps.write('.'))
      .pipe(gulp.dest(path.build.style))
      .on('error', console.log)
      .pipe(reload({stream: true}));
});

gulp.task('compile:js', function() {
    return gulp.src(path.assets.js)
        .pipe(sourcemaps.init())
        .pipe( babel({ loose: 'all' }) ).on('error', console.log)
        .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.js))
        .pipe(reload({stream: true}));
});

gulp.task('compile:images', function() {
    return gulp.src(path.assets.img)
        //.pipe(imagemin({
        //    progressive: true,
        //    svgoPlugins: [{removeViewBox: false}],
        //    use: [pngquant()],
        //    interlaced: true
        //}))
        .pipe(gulp.dest(path.build.img))
        .pipe(reload({stream: true}));
});

gulp.task('compile', ['compile:css', 'compile:js', 'compile:images']);


gulp.task('watch', function() {
    gulp.run('compile');

    gulp.watch(path.assets.style, function() {
        gulp.run('compile:css');
    });
    gulp.watch(path.assets.js, function() {
        gulp.run('compile:js');
    });
    gulp.watch(path.assets.img, function() {
        gulp.run('compile:images');
    });

});

gulp.task('clean', function (cb) {
    rimraf(path.clean, cb);
});

gulp.task('default', ['compile', 'watch'])
