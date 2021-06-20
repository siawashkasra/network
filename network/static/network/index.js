window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

   

});

let current_record = 0

function edit_post(post_id) {

    let id = post_id.split(/(\d+)/);
    let content = document.querySelector("#cont" + String(id[1])).innerHTML
    // document.querySelector("#edit_content").innerHTML = content
    current_record = id[1]
}


document.querySelector("#update").addEventListener("submit", function(event){
    event.preventDefault()

    var formData = new FormData(document.querySelector('#update'))

    document.querySelector("#cont" + String(current_record)).innerHTML = formData.get("content")
    document.querySelector("#edit_content").value = ''
    $('#edit_post').modal('hide');
    update_post(current_record, {'content': formData.get("content")})
});


function update_post(id, data) {
    fetch('/post/update/' + id, {
        method: 'PUT', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            })
            .catch((error) => {
            console.error('Error:', error);
            });
}


function like(x) {
    count = document.querySelector("#p" + String(x.id)).innerHTML
    count = parseInt(count) + 1
    document.querySelector("#p" + String(x.id)).innerHTML = String(count)
    update_like(x.id)
    x.classList.toggle("btn-info")

}

function update_like(pid) {
    
    fetch('/post/like/' + pid, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            })
            .catch((error) => {
            console.error('Error:', error);
            });
}


function unlike(x) {
    count = document.querySelector("#p" + String(x.id)).innerHTML
    count = parseInt(count) - 1
    document.querySelector("#p" + String(x.id)).innerHTML = String(count)
    update_unlike(x.id)
    x.classList.toggle("btn-info")
}


function update_unlike(pid) {
    
    fetch('/post/unlike/' + pid, {
        method: 'PUT', // or 'POST'
        headers: {
            'Content-Type': 'application/json',
        },
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            })
            .catch((error) => {
            console.error('Error:', error);
            });
}