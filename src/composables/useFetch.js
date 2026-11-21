import { ref } from 'vue'

export function useFetch(url) {
  // Reactive references to hold the data, loading state, and error message   
  const data    = ref(null)
  const loading = ref(true)
  const error   = ref(null)

  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      return res.json()
    })
    .then(json => { data.value = json })
    .catch(e  => { error.value = e.message })
    .finally(() => { loading.value = false })

  return { data, loading, error }
}