document.addEventListener('DOMContentLoaded', ()=> {
    const likeBtns = document.querySelectorAll('.toggle-like');
    likeBtns.forEach((likeBtn) => {
        likeBtn.onclick = ()=> {
            const postId = likeBtn.dataset.likeId;
            const likeText = likeBtn.textContent;
            const likeCountText = document.querySelector(`[data-likes-id="${postId}"]`).textContent;
            const likeCount = parseInt(likeCountText);
            

            /* Sanity check that view is working */ 
            
            // fetch(`/like/${postId}`)
            // .then(response => response.json())
            // .then(result => {
            //     console.log(result);
            // });
            

            /* Handle POST request */
            form = new FormData()
            form.append("field", likeText);
            form.append("likes", likeCount);
            fetch(`/like/${postId}`, {
                method: 'POST',
                body: JSON.stringify(form)
            })
            .then(response => response.json())
            .then(response => {
                if (response.field === 'Like'){
                    likeBtn.textContent = 'Unlike';
                    likeBtn.setAttribute('class', 'btn btn-sm btn-danger');
                }
                else {
                    likeBtn.textContent = 'Like';
                    likeBtn.setAttribute('class', 'btn btn-sm btn-success');
                }
                document.querySelector(`[data-likes-id="${postId}"]`).textContent = response.likes;
            });

        }
            
    })
});

