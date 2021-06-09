<template>
  <div style="width:100%">
    <v-dialog
      v-model="dialog"
      width="700px"
    >
      <v-card>
        <a
          :href="`${imageRoot}${focusImgID}`"
          target="_blank"
        >
          <v-img
            :src="`${imageRoot}${focusImgID}`"
          />
        </a>
        <ImageUrls class="ma-2" />
        <p class="ma-2">
          Image Description
        </p>
        <v-divider />
        <v-card-title>
          Similar Images
        </v-card-title>
        <v-row
          v-for="n in Math.ceil(similarImgIDs.length/4) "
          :key="n"
          style="width:100%;margin:0 auto;"
        >
          <v-col
            v-for="nn in 4"
            :key="nn"
            style="width:20%;margin:0 auto;"
          >
            <div v-if="(nn-1)+(n-1)*4<similarImgIDs.length">
              <a
                :href="`${imageRoot}${similarImgIDs[(nn-1)+(n-1)*4]}`"
                target="_blank"
              >
                <v-img
                  :src="`${imageRoot}${similarImgIDs[(nn-1)+(n-1)*4]}&size=100*100`"
                  height="100px"
                />
              </a>
              <ImageUrls />
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
    <v-row
      v-for="n in Math.ceil(searchImgIDs.length/4) "
      :key="n"
      style="width:100%;margin:0 auto;"
    >
      <v-col
        v-for="nn in 4"
        :key="nn"
        style="width:20%;margin:0 auto;"
      >
        <div v-if="(nn-1)+(n-1)*4<searchImgIDs.length">
          <v-img
            :src="`${imageRoot}${searchImgIDs[(nn-1)+(n-1)*4]}&size=300*300`"
            height="300px"
            class="hover-pointer"
            @click="focusImgID=searchImgIDs[(nn-1)+(n-1)*4]; dialog=true"
          />
          <ImageUrls />
        </div>
      </v-col>
    </v-row>
    <div class="text-center ma-10">
      <div
        style="margin-bottom:1em;"
      >
        {{ `${totalNum} results in ${lastQueryTime.toFixed(2)} ms` }}
      </div>
      <v-pagination
        v-model="page"
        :length="totalPage"
        circle
        :total-visible="9"
      />
    </div>
    <template>
      <div class="vld-parent">
        <loading
          :active.sync="loading"
          :is-full-page="true"
        />
      </div>
    </template>
  </div>
</template>

<script>
import ImageUrls from '@/components/ImageUrls'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'

export default {
  components: {
    ImageUrls,
    Loading
  },
  data () {
    return {
      page: 1,
      focusImgID: '',
      dialog: false,
      searchImgIDs: [],
      similarImgIDs: [],
      totalNum: 0,
      lastQueryTime: 0,
      totalPage: 1,
      imageRoot: 'http://127.0.0.1:8000/api/image?image=',
      loading: false
    }
  },
  watch: {
    '$route.query' () {
      this.init()
    },
    page (newPage) {
      const queryObj = Object.assign({}, this.$route.query, { page: newPage })
      this.$router.push({
        path: '/search/',
        query: queryObj
      })
    },
    dialog () {
      this.similarImgIDs = []
      this.$axios.get('/api/similar', {
        params: {
          image: this.focusImgID,
          num: 20
        }
      }).then(
        (res) => {
          const { data } = res.data
          this.similarImgIDs = data.images
        }
      )
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      this.loading = true
      const queryObj = this.$route.query
      const start = performance.now()
      this.$axios.get('/api/search', { params: queryObj }).then(
        (res) => {
          this.lastQueryTime = performance.now() - start
          if (res.data.code !== 200) {
            return this.$nuxt.error({ message: res.data.msg })
          }
          const { data } = res.data
          this.totalNum = data.total
          this.totalPage = Math.floor((data.total - 1) / data.num) + 1
          this.page = data.page
          this.searchImgIDs = data.images
          this.loading = false
        }, (msg) => {
          return this.$nuxt.error({ message: msg })
        }
      )
    }
  }
}
</script>

<style>
.hover-pointer:hover {
  cursor: pointer;
}
</style>
