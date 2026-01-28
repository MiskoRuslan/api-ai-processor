// Pokemon AI Processor - Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pokemonForm');
    const countInput = document.getElementById('count');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const resultsContainer = document.getElementById('resultsContainer');

    // Form submission handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const count = parseInt(countInput.value);

        // Validate input
        if (!count || count < 1 || count > 20) {
            showError('Please enter a number between 1 and 20');
            return;
        }

        // Clear previous results and errors
        hideError();
        hideResults();

        // Show loading state
        showLoading();
        disableForm();

        try {
            // Make API request
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ count: count })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to process request');
            }

            const data = await response.json();

            // Display results
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred while processing your request');
        } finally {
            hideLoading();
            enableForm();
        }
    });

    // Input validation on change
    countInput.addEventListener('input', () => {
        const value = parseInt(countInput.value);
        if (value && (value < 1 || value > 20)) {
            countInput.setCustomValidity('Number must be between 1 and 20');
        } else {
            countInput.setCustomValidity('');
        }
    });

    /**
     * Display results in cards
     */
    function displayResults(data) {
        resultsContainer.innerHTML = '';

        if (!data || data.length === 0) {
            resultsContainer.innerHTML = '<p>No results found</p>';
            showResults();
            return;
        }

        data.forEach((pokemon, index) => {
            const card = createPokemonCard(pokemon, index);
            resultsContainer.appendChild(card);
        });

        showResults();
    }

    /**
     * Create a pokemon card element
     */
    function createPokemonCard(pokemon, index) {
        const card = document.createElement('div');
        card.className = 'pokemon-card';
        card.style.animationDelay = `${index * 0.1}s`;

        const name = document.createElement('h3');
        name.textContent = pokemon.item;

        const description = document.createElement('p');
        description.textContent = pokemon.result;

        card.appendChild(name);
        card.appendChild(description);

        return card;
    }

    /**
     * Show error message
     */
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    /**
     * Hide error message
     */
    function hideError() {
        errorDiv.classList.add('hidden');
        errorDiv.textContent = '';
    }

    /**
     * Show loading state
     */
    function showLoading() {
        loadingDiv.classList.remove('hidden');
    }

    /**
     * Hide loading state
     */
    function hideLoading() {
        loadingDiv.classList.add('hidden');
    }

    /**
     * Show results section
     */
    function showResults() {
        resultsDiv.classList.remove('hidden');
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Hide results section
     */
    function hideResults() {
        resultsDiv.classList.add('hidden');
    }

    /**
     * Disable form during submission
     */
    function disableForm() {
        submitBtn.disabled = true;
        countInput.disabled = true;
        btnText.textContent = 'Processing...';
        btnLoader.classList.remove('hidden');
    }

    /**
     * Enable form after submission
     */
    function enableForm() {
        submitBtn.disabled = false;
        countInput.disabled = false;
        btnText.textContent = 'Process Pokemon';
        btnLoader.classList.add('hidden');
    }
});
