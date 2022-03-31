import Axios from "axios"
export function get(url){
    return Axios.get(url)
}
export function post(url,params){
    return Axios.post(url,params)
}
export function put(url,params){
    return Axios.put(url,params)
}
export function del(url){
    return Axios.delete(url)
}