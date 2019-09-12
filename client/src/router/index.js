import Vue from 'vue'
import Router from 'vue-router'
import Account from '@/components/Account'
import Rhino from '@/components/Rhino'
import Jobs from '@/components/jobs/Jobs'
import Job from '@/components/jobs/Job'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Account',
      component: Account
    },
    {
      path: '/rhino',
      name: 'Rhino',
      component: Rhino
    },
    {
      path: '/:resourceName/jobs',
      name: 'Jobs',
      component: Jobs
    },
    {
      path: '/:resourceName/job/:jobId',
      name: 'Job',
      component: Job
    },
  ],
})
