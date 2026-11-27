import { API } from '../constants.js'

// GET a path and return its JSON (throws if the server says no)
export async function getJSON(path) {
    const res = await fetch(`${API}${path}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.json()
}

// POST / PUT / DELETE. Returns the JSON reply, or throws an Error with the server's message.
export async function send(method, path, body) {
    const res = await fetch(`${API}${path}`, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : undefined,
    })
    if (!res.ok) {
        let message = `HTTP ${res.status}`
        try {
            const err = await res.json()
            if (typeof err.detail === 'string') message = err.detail            // 404 / 409
            else if (Array.isArray(err.detail)) {                                // 422
                message = err.detail.map(d => `${d.loc.at(-1)}: ${d.msg}`).join(', ')
            }
        } catch { /* not JSON */ }
        throw new Error(message)
    }
    return res.status === 204 ? null : res.json()    // 204 = no body
}