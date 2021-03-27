document.addEventListener('DOMContentLoaded', function() {

    if(document.contains(document.querySelector(".post"))) {

        document.querySelector('.post').addEventListener('submit', post);
    }
  
    // By default, load the 10 recent posts
    load_posts();
  });

  function post(event) {
    event.preventDefault();

    fetch('post', {
        method: 'POST',
        body: JSON.stringify({
        
            content: document.querySelector("#content").value,
        })
    })

    .then(response =>  {
        if (response.status == 200) {
            console.log("It worked")
        }
        
    })
  }


  function load_posts() {

    fetch('posts' , {
        method: 'GET',
        headers : { 
          'Accept': 'application/json'
        }
    })
        
    .then(response => response.json())
    .then(post => {

        document.querySelector(".card-title").textContent = post[0].user
        document.querySelector(".timestamp").textContent = post[0].timestamp
        document.querySelector(".content").textContent = post[0].content
        console.log(post[0])
  });
}