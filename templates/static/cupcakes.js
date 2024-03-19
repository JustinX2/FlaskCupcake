async function getCupcakes(){
    const response=await axios.get('/api/cupcakes');
    return response.data.cupcakes;
}

function displayCupcakes(cupcakes){
    const list=document.getElementById('cupcake-list');
    list.innerHTML=cupcakes.map(function(cupcake){
        return `
            <li>
                ${cupcake.flavor} - Size: ${cupcake.size}, Rating: ${cupcake.rating}
                ${cupcake.image ? `<img src="${cupcake.image}" width="100">` : ''}
            </li>
        `;
    }).join('')
}

document.getElementById('new-cupcake-form').addEventListener('submit', async function(e){
    e.preventDefault();
    const flavor=document.getElementById('flavor').value;
    const size=document.getElementById('size').value;
    const rating=document.getElementById('rating').value;
    const image=document.getElementById('image').value || null;

    try {
        await axios.post('/api/cupcakes', {flavor, size, rating, image});
        const cupcakes=await getCupcakes();
        displayCupcakes(cupcakes);
    } catch (error){
        console.error("There was an error in creating cupcake", error);
    }
})
