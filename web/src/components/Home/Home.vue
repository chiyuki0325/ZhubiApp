<script setup>
// 自动跳转到 /login 或 /chat
import {api} from '@/utils'
import Cookies from "js-cookie"
import {useRouter} from "vue-router"

const router = useRouter()
if (Cookies.get('token')) {
  api.post('/user/validate', {
    token: Cookies.get('token')
  }).then(res => {
    if (res.data.valid === true) {
      router.push('/chat')
    } else {
      router.push('/login')
    }
  })
} else {
  router.push('/login')
}
</script>
