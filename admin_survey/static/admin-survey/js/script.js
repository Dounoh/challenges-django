        // Données pour les graphiques
        const pollData = {
            labels: ['Sondage 1', 'Sondage 2', 'Sondage 3', 'Sondage 4', 'Sondage 5'],
            datasets: [{
                label: 'Votes',
                data: [120, 300, 150, 400, 250],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };

        const userData = {
            labels: ['Utilisateurs A', 'Utilisateurs B', 'Utilisateurs C'],
            datasets: [{
                label: 'Participation',
                data: [45, 30, 25],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        };

        // Initialisation des Graphiques
        const pollVotesChartCtx = document.getElementById('pollVotesChart').getContext('2d');
        const userParticipationChartCtx = document.getElementById('userParticipationChart').getContext('2d');

        new Chart(pollVotesChartCtx, {
            type: 'bar',
            data: pollData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Votes par Sondage',
                    },
                },
            },
        });

        new Chart(userParticipationChartCtx, {
            type: 'doughnut',
            data: userData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Participation des Utilisateurs',
                    },
                },
            },
        });



// *********************************************
// LA PARTIE POUR LA CREATION DES SONDAGES
// *********************************************

