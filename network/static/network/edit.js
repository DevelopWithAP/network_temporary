document.addEventListener('DOMContentLoaded', () => {
   let editBtns = document.querySelectorAll('.show-edit');
   editBtns.forEach(function(editBtn){
       editBtn.onclick = ()=> {
        let postId = editBtn.dataset.editId;
        let content = document.querySelector(`[data-post-content-id="${postId}"]`);
        let editDiv = document.querySelector(`[data-edit-div-id="${postId}"]`);
        let editArea = document.querySelector(`[data-edit-area-id="${postId}"]`);
        
        content.style.display = 'none';
        editDiv.style.display = 'block';
        editArea.value = content.innerHTML;
    }

    let closeBtns = document.querySelectorAll('.close-edit');
    closeBtns.forEach((closeBtn)=> {
        closeBtn.addEventListener('click', ()=>{
            let postId = closeBtn.dataset.closeEditId;
            let content = document.querySelector(`[data-post-content-id="${postId}"]`);
            let editDiv = document.querySelector(`[data-edit-div-id="${postId}"]`);

            content.style.display = 'block';
            editDiv.style.display = 'none';
        })
    })

    let editBtns = document.querySelectorAll('.save-edit');
    editBtns.forEach((editBtn)=> {
        editBtn.onclick = ()=> {
            let postId = editBtn.dataset.saveEditId;
            let content = document.querySelector(`[data-post-content-id="${postId}"]`);
            let editDiv = document.querySelector(`[data-edit-div-id="${postId}"]`);
            let new_content = document.querySelector(`[data-edit-area-id="${postId}"]`);
            if(new_content.value.length != 0){
                fetch(`edit/${postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: new_content.value
                    })
                });
            }
            editDiv.style.display = 'none';
            content.innerHTML = new_content.value;
            content.style.display = 'block';
        }
    })

   });
    


});
