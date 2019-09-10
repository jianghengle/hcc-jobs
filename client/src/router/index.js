import Vue from 'vue'
import Router from 'vue-router'
import Account from '@/components/Account'
import About from '@/components/About'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Account',
      component: Account
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
  ],
})
