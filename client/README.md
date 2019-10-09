# client

The front end is [Vue.js](https://vuejs.org/) project. It can consume multiple cluster backends but provide a single uniform interface.

Modify the file `src/store/modules/info.js` to configure which the cluster backend(s) to be used. Please remember add caches for each cluster like the existing `rhino`.

Modify the files `src/components/MyMenu.vue` and `src/components/MyHeader.vue` to work with your clusters, and/or add new components like `src/components/Rhino.vue` and put it in the router `src/router/index.js` as you want. 

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

Except for Vue core package, it also uses [Vuex](https://vuex.vuejs.org/) for state management, [Vue Router](https://router.vuejs.org/) for frontend router, and [Vue Resource](https://github.com/pagekit/vue-resource) to make AJAX calls.

CSS framework is using [Bulma](https://bulma.io/).

Using [Echart](https://echarts.apache.org/examples/en/) to draw the CPU and memory charts.

The web code editor is using [Vue Prism Editor](https://github.com/koca/vue-prism-editor).

