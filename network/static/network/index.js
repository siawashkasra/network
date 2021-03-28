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
            document.querySelector("#content").value ='',
            load_posts();
        }
        
    })
  }


  function load_posts() {
    clear_DOM()

    fetch('posts' , {
        method: 'GET',
        headers : { 
          'Accept': 'application/json'
        }
    })
        
    .then(response => response.json())
    .then(posts => {

        console.log(posts)
        for (let post = 0; post < posts.length; post++) {
            create_post_view(posts[post])
        }
  });
}


function create_post_view(post) {
    
    const div_card = document.createElement("div")
    div_card.classList.add("card")
    div_card.classList.add("mb-3")

    const div_parent_row = document.createElement("div")
    div_parent_row.classList.add("row")
    div_parent_row.classList.add("g-0")

    const div_child_row = document.createElement("div")
    div_child_row.classList.add("row")

    const div_col_md_2 = document.createElement("div")
    div_col_md_2.classList.add("col-md-2")

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svg.setAttribute("height", "50")
    svg.setAttribute("width", "50")

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g")

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle")
    circle.setAttribute("cx", "30")
    circle.setAttribute("cy", "30")
    circle.setAttribute("r", "20")
    circle.setAttribute("fill", fill="#0dcaf0")

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text")
    text.setAttribute("x", "20")
    text.setAttribute("y", "35")
    text.setAttribute("font-family", "Times")
    text.setAttribute("fill", "white")
    text.textContent = get_initials(post.first_name, post.last_name)

    const div_col_md_10 = document.createElement("div")
    div_col_md_10.classList.add("col-md-10")

    const h6 = document.createElement("h6")
    h6.classList.add("card-title")
    h6.textContent = post.user

    const p = document.createElement("p")
    p.classList.add("card-text")
    p.classList.add("timestamp")

    const small = document.createElement("small")
    small.classList.add("text-muted")
    small.textContent = get_time(post.timestamp)

    const col = document.createElement("div")
    col.classList.add("col")

    const card_body = document.createElement("div")
    card_body.classList.add("card-body")

    const card_text = document.createElement("p")
    card_text.classList.add("card-text")
    card_text.classList.add("content")
    card_text.textContent = post.content


    g.appendChild(circle)
    g.appendChild(text)
    svg.appendChild(g)
    div_col_md_2.appendChild(svg)
    div_child_row.appendChild(div_col_md_2)

    div_col_md_10.appendChild(h6)

    p.appendChild(small)
    div_col_md_10.appendChild(p)
    div_child_row.appendChild(div_col_md_10)
    div_parent_row.appendChild(div_child_row)

    card_body.appendChild(card_text)
    col.appendChild(card_body)
    div_parent_row.appendChild(col)

    div_card.appendChild(div_parent_row)

    if (document.contains(document.querySelector("#placeholder"))) {

        target = document.querySelector("#placeholder")
        target.after(div_card)
    }
    

}


function clear_DOM() {

    if(document.contains(document.querySelector(".card"))) {
      
      emails = document.querySelectorAll(".card")
  
        emails.forEach(element => {
  
          element.remove()
  
        });
      }
        
    }


function get_initials(first_name, last_name) {
    first = first_name.substr(0, 1); 
    last = last_name.substr(0, 1); 

    return first + last

}


function get_time(po_time) {
    return new Date(po_time).toDateString()
}