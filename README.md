<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>FANJAKA</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: "Courier New", monospace;
            color: #00ff00;
            overflow: hidden;
        }

        /* Effet scanline */
        body::before {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                to bottom,
                rgba(0, 255, 0, 0.05),
                rgba(0, 255, 0, 0.05) 1px,
                transparent 1px,
                transparent 3px
            );
            pointer-events: none;
        }

        .terminal {
            border: 2px solid #00ff00;
            padding: 30px 50px;
            box-shadow: 0 0 20px #00ff00;
            text-align: center;
        }

        .title {
            font-size: 2.5rem;
            letter-spacing: 4px;
            animation: flicker 2s infinite;
        }

        .subtitle {
            margin-top: 15px;
            font-size: 1.2rem;
            opacity: 0.8;
        }

        @keyframes flicker {
            0% { opacity: 1; }
            5% { opacity: 0.7; }
            10% { opacity: 1; }
            15% { opacity: 0.5; }
            20% { opacity: 1; }
            100% { opacity: 1; }
        }

        /* Curseur clignotant */
        .cursor::after {
            content: "_";
            animation: blink 1s steps(2, start) infinite;
        }

        @keyframes blink {
            to { visibility: hidden; }
        }
    </style>
</head>
<body>

    <div class="terminal">
        <div class="title cursor">
            FANJAKA SOA KAHE
        </div>
        <div class="subtitle">
            &gt; system access granted
        </div>
    </div>

</body>
</html>

