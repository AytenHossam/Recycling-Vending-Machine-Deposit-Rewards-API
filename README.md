# Recycling Vending Machine (RVM) Platform API

## Technologies
- Django
- Django REST Framework
- SQLite 
- SimpleJWT -> token authentication

## Setup Instructions

1. **Clone the repo & navigate to project**
2. **Create virtual environment & install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install django djangorestframework djangorestframework-simplejwt
   ```
3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Create superuser (for admin panel):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Endpoints

#### **No Authentication Required:**
- `POST /api/register/` — > Register user (`username`, `email`, `password`)
- `POST /api/login/` — > Login with `email` & `password` (returns JWT tokens)
- `GET /api/deposit-info/` — > Public info: available machines & reward rates

#### **JWT Authentication Required:**
- `POST /api/deposit/` — > Log deposit
  - `material_type`: "plastic", "metal", "glass"
  - `weight`: float (kg)
  - `machine_id`: int
- `GET /api/summary/` — > Get recycling summary by material type

### Admin Endpoints

#### **No Authentication Required:**
- `POST /api/admin/register/` — > Register admin (`username`, `email`, `company_id`, `password`)
- `POST /api/admin/login/` — > Login with `username` & `password` (returns JWT tokens, only for admins)

#### **Admin JWT Authentication Required:**
- `GET /api/machines/` — > List all machines (admin only)
- `POST /api/machines/` — > Add new machine (admin only)
  - **Body:** `{"location": "Lobby", "status": "active"}`
- `GET /api/admin/deposits/` — > View all deposits (admin only)


## Reward Points Calculation
- Plastic: 1 point/kg
- Metal: 3 points/kg
- Glass: 2 points/kg
- **Points are calculated as floats and wrote down to the nearest 1st decimal**
- Example: 1.88999987 kg plastic = 1.8 points

## Authentication Flow
- **Users:** Register, login, receive JWT tokens, use `Authorization: Bearer <token>` header for all requests.
- **Admins:** Register, login, must have `is_staff=True`, use JWT tokens as above. Only admins can access `/machines/` and `/admin/` endpoints.

## Notes
- All usernames are unique.
- Only valid material types are accepted.
- Users can only see their deposit summary.
- Admins can add machines and view all deposits.
- Points are stored as floats and rounded to 1 decimal place for precision.

## Testing Workflow
**Before testing the user part it's better to first register or log in as an admin then add a machine. This way, when a user wants to deposit something, there will be a machine to choose from using its machineID.**

If you're not sure whether machines already exist, just do a GET request to `/api/deposit-info/` — it will show you the list of machines you can use for deposits. 
