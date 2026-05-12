from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# ── Health Check ──────────────────────────────────────────────────────────────

@api_view(['GET'])
def health_check(request):
    """Kubernetes liveness/readiness probe endpoint."""
    return Response({'status': 'ok'})


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(['POST'])
def signup(request):
    """
    POST /api/signup/
    Body: { username, email, password, password2 }
    """
    username = request.data.get('username', '').strip()
    email    = request.data.get('email', '').strip()
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)
    if password != password2:
        return Response({'error': 'Passwords do not match.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'Account created successfully.'}, status=201)


@api_view(['POST'])
def login_view(request):
    """
    POST /api/login/
    Body: { username, password }
    Returns: { access, refresh, username }
    """
    username = request.data.get('username', '')
    password = request.data.get('password', '')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid username or password.'}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access':    str(refresh.access_token),
        'refresh':   str(refresh),
        'username':  user.username,
        'is_staff':  user.is_staff,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/logout/
    Header: Authorization: Bearer <access_token>
    Body:   { refresh: <refresh_token> }
    Blacklists the refresh token (client should discard the access token).
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass  # Token may already be invalid; that's fine
    return Response({'message': 'Logged out.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """GET /api/me/ — Returns current user info."""
    return Response({
        'username': request.user.username,
        'email':    request.user.email,
        'is_staff': request.user.is_staff,
    })


# ── Charts / Calendar data ────────────────────────────────────────────────────

@api_view(['GET'])
def symbols(request):
    """GET /api/symbols/ — Returns the preset trading symbol list."""
    data = {
        'Cryptocurrencies': [
            {'label': 'Bitcoin (BTC/USDT)',   'value': 'BINANCE:BTCUSDT'},
            {'label': 'Ethereum (ETH/USDT)',  'value': 'BINANCE:ETHUSDT'},
            {'label': 'BNB (BNB/USDT)',       'value': 'BINANCE:BNBUSDT'},
            {'label': 'Solana (SOL/USDT)',     'value': 'BINANCE:SOLUSDT'},
            {'label': 'XRP (XRP/USDT)',        'value': 'BINANCE:XRPUSDT'},
        ],
        'Forex': [
            {'label': 'EUR/USD', 'value': 'OANDA:EURUSD'},
            {'label': 'USD/JPY', 'value': 'OANDA:USDJPY'},
            {'label': 'GBP/USD', 'value': 'OANDA:GBPUSD'},
            {'label': 'USD/CHF', 'value': 'OANDA:USDCHF'},
            {'label': 'AUD/USD', 'value': 'OANDA:AUDUSD'},
        ],
        'Stocks': [
            {'label': 'Apple (AAPL)',     'value': 'NASDAQ:AAPL'},
            {'label': 'Tesla (TSLA)',     'value': 'NASDAQ:TSLA'},
            {'label': 'Microsoft (MSFT)', 'value': 'NASDAQ:MSFT'},
            {'label': 'Amazon (AMZN)',    'value': 'NASDAQ:AMZN'},
            {'label': 'NVIDIA (NVDA)',    'value': 'NASDAQ:NVDA'},
        ],
        'Indices': [
            {'label': 'Nasdaq 100 (NAS100)', 'value': 'OANDA:NAS100USD'},
            {'label': 'S&P 500 (SPX500)',    'value': 'OANDA:SPX500USD'},
            {'label': 'Dow Jones (US30)',     'value': 'OANDA:US30USD'},
            {'label': 'Nikkei 225',          'value': 'OANDA:JP225USD'},
            {'label': 'FTSE 100 (UK)',        'value': 'OANDA:UK100GBP'},
        ],
        'Commodities': [
            {'label': 'Gold (XAU/USD)',   'value': 'TVC:GOLD'},
            {'label': 'Silver (XAG/USD)', 'value': 'TVC:SILVER'},
            {'label': 'Crude Oil WTI',    'value': 'TVC:USOIL'},
            {'label': 'Crude Oil Brent',  'value': 'TVC:UKOIL'},
        ],
    }
    return Response(data)


@api_view(['GET'])
def calendar_events(request):
    """GET /api/calendar/ — Returns economic calendar events."""
    events = [
        {'time': '08:30 AM', 'event': 'Non Farm Payrolls',       'currency': 'USD', 'impact': 'High'},
        {'time': '10:00 AM', 'event': 'ISM Manufacturing PMI',   'currency': 'USD', 'impact': 'Medium'},
        {'time': '04:00 AM', 'event': 'ECB Interest Rate Decision', 'currency': 'EUR', 'impact': 'High'},
        {'time': '12:30 PM', 'event': 'Crude Oil Inventories',   'currency': 'USD', 'impact': 'Low'},
    ]
    return Response(events)
