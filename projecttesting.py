import re
from typing import Dict, List, Optional
from datetime import datetime

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="MyCar Advisor Malaysia",
    page_icon="🚗",
    layout="wide",
)


CAR_DATABASE: List[Dict] = [
    {
        "name": "Perodua Myvi 1.5 AV",
        "brand": "Perodua",
        "type": "Hatchback",
        "price_rm": 59500,
        "seats": 5,
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 21.1,
        "boot_space_l": 277,
        "maintenance_level": "Low",
        "best_for": ["city driving", "students", "first car", "low maintenance", "fuel saving"],
        "pros": [
            "Affordable ownership cost",
            "Easy to drive in Malaysian cities",
            "Good fuel efficiency",
            "Strong resale value",
        ],
        "cons": [
            "Limited boot space for large families",
            "Not ideal for frequent long-distance cargo use",
        ],
        "why_this_car": "The Myvi is a practical all-rounder for Malaysians who want low running cost, easy parking, and dependable daily transport.",
        "usage_recommendation": "Best for daily city commutes, campus travel, and small families that want good fuel savings.",
        "maintenance_advice": [
            "Service engine oil and filter every 10,000 km or as stated in the service booklet.",
            "Check tyre pressure monthly because city driving and hot weather can affect it.",
            "Rotate tyres every 10,000 km to maintain even wear.",
            "Inspect battery health before festive long-distance travel.",
        ],
    },
    {
        "name": "Perodua Bezza 1.3 AV",
        "brand": "Perodua",
        "type": "Sedan",
        "price_rm": 49980,
        "seats": 5,
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 22.0,
        "boot_space_l": 508,
        "maintenance_level": "Low",
        "best_for": ["e-hailing", "fuel saving", "budget buyers", "city driving", "small family"],
        "pros": [
            "Very fuel efficient",
            "Large boot for a budget sedan",
            "Low maintenance cost",
            "Practical for e-hailing use",
        ],
        "cons": [
            "Simple cabin design",
            "Performance is focused on efficiency, not sporty driving",
        ],
        "why_this_car": "The Bezza suits owners who prioritize fuel savings, low monthly cost, and a useful sedan boot for daily tasks.",
        "usage_recommendation": "Recommended for budget-conscious drivers, Grab drivers, and owners who do a lot of daily mileage.",
        "maintenance_advice": [
            "Monitor brake pad wear more often if used for e-hailing or heavy urban traffic.",
            "Keep the cabin air filter clean because frequent city use can build up dust quickly.",
            "Use regular scheduled servicing to preserve fuel economy.",
            "Check alignment after pothole impacts during rainy seasons.",
        ],
    },
    {
        "name": "Proton Saga 1.3 Premium S",
        "brand": "Proton",
        "type": "Sedan",
        "price_rm": 44800,
        "seats": 5,
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 15.2,
        "boot_space_l": 420,
        "maintenance_level": "Low",
        "best_for": ["budget buyers", "first car", "small family", "highway driving"],
        "pros": [
            "Affordable purchase price",
            "Comfortable ride quality",
            "Stable for highway use",
            "Spacious enough for daily family use",
        ],
        "cons": [
            "Fuel economy is not class-leading",
            "Interior technology is more basic than newer models",
        ],
        "why_this_car": "The Saga is a strong value choice when comfort and purchase price matter more than advanced features.",
        "usage_recommendation": "Good for first-time owners, family errands, and mixed town-highway driving on a tight budget.",
        "maintenance_advice": [
            "Inspect suspension and tyres regularly if driving on uneven roads.",
            "Change engine oil according to service intervals to protect long-term reliability.",
            "Watch coolant level before long balik kampung trips.",
            "Clean wiper blades and check washer fluid during monsoon periods.",
        ],
    },
    {
        "name": "Proton X50 1.5 TGDi Flagship",
        "brand": "Proton",
        "type": "SUV",
        "price_rm": 113300,
        "seats": 5,
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 15.3,
        "boot_space_l": 330,
        "maintenance_level": "Medium",
        "best_for": ["young professionals", "small family", "highway driving", "technology lovers"],
        "pros": [
            "Modern safety and infotainment features",
            "Strong turbocharged performance",
            "Comfortable elevated driving position",
            "Popular compact SUV choice in Malaysia",
        ],
        "cons": [
            "Higher ownership cost than entry-level cars",
            "Rear space is less generous than larger SUVs",
        ],
        "why_this_car": "The X50 stands out for drivers who want a stylish SUV feel, advanced features, and stronger performance for mixed city-highway use.",
        "usage_recommendation": "Recommended for professionals or small families who want comfort, safety tech, and occasional interstate travel ability.",
        "maintenance_advice": [
            "Use quality fuel and follow turbo-engine servicing intervals closely.",
            "Check tyres and brakes before long highway journeys because the vehicle is often driven faster.",
            "Keep software and infotainment updates current through authorized service centers when available.",
            "Inspect air-conditioning performance regularly in hot weather conditions.",
        ],
    },
    {
        "name": "Honda City 1.5 RS e:HEV",
        "brand": "Honda",
        "type": "Sedan",
        "price_rm": 111900,
        "seats": 5,
        "transmission": "e-CVT",
        "fuel_type": "Hybrid",
        "fuel_economy_km_l": 27.8,
        "boot_space_l": 519,
        "maintenance_level": "Medium",
        "best_for": ["fuel saving", "professionals", "small family", "technology lovers", "city driving"],
        "pros": [
            "Excellent fuel efficiency",
            "Smooth urban driving experience",
            "Large boot space",
            "Good safety package",
        ],
        "cons": [
            "Higher upfront price",
            "Hybrid system may be less familiar to some owners",
        ],
        "why_this_car": "The City e:HEV makes sense for owners who drive often in traffic and want premium efficiency without moving to a larger SUV.",
        "usage_recommendation": "Best for urban commuters and professionals who want lower fuel use with sedan practicality.",
        "maintenance_advice": [
            "Follow Honda hybrid service intervals carefully.",
            "Have the high-voltage system checked only by qualified technicians.",
            "Keep 12V battery and software diagnostics in good condition.",
            "Maintain proper tyre pressure to maximize hybrid efficiency.",
        ],
    },
    {
        "name": "Toyota Corolla Cross 1.8V",
        "brand": "Toyota",
        "type": "SUV",
        "price_rm": 137000,
        "seats": 5,
        "transmission": "CVT",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 15.4,
        "boot_space_l": 440,
        "maintenance_level": "Medium",
        "best_for": ["family", "highway driving", "comfort", "suv buyers", "daily use"],
        "pros": [
            "Comfortable and practical family SUV",
            "Strong reliability image",
            "Good ride height and visibility",
            "Reasonable boot space",
        ],
        "cons": [
            "More expensive than local-brand alternatives",
            "Not the sportiest option in its segment",
        ],
        "why_this_car": "The Corolla Cross is a sensible SUV pick for buyers who value comfort, reliability, and easy everyday family usability.",
        "usage_recommendation": "Recommended for family commuting, school runs, and comfortable weekend highway trips.",
        "maintenance_advice": [
            "Service CVT fluid according to Toyota guidance.",
            "Inspect tyres, especially if frequently carrying passengers and luggage.",
            "Clean the cabin filter and air-con system regularly in humid conditions.",
            "Check brake condition before long holiday travel.",
        ],
    },
    {
        "name": "Mitsubishi Xpander Plus",
        "brand": "Mitsubishi",
        "type": "MPV",
        "price_rm": 99800,
        "seats": 7,
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 14.5,
        "boot_space_l": 495,
        "maintenance_level": "Medium",
        "best_for": ["large family", "7-seater", "school runs", "road trips", "flexible seating"],
        "pros": [
            "Seven-seat practicality",
            "Flexible cabin arrangement",
            "Comfortable family-focused ride",
            "Good value for a people mover",
        ],
        "cons": [
            "Less powerful when fully loaded",
            "Fuel use is higher than compact sedans",
        ],
        "why_this_car": "The Xpander is a practical answer for Malaysian families who need extra seats without moving to a very expensive SUV.",
        "usage_recommendation": "Best for parents, carpooling, family trips, and owners who need flexible seat folding for cargo.",
        "maintenance_advice": [
            "Check rear tyre and brake wear because MPVs often carry heavier loads.",
            "Inspect suspension if the car is regularly used with full passengers.",
            "Clean air vents and rear cabin areas to keep passenger comfort high.",
            "Check spare tyre condition before interstate trips.",
        ],
    },
    {
        "name": "Perodua Alza 1.5 AV",
        "brand": "Perodua",
        "type": "MPV",
        "price_rm": 75800,
        "seats": 7,
        "transmission": "D-CVT",
        "fuel_type": "Petrol",
        "fuel_economy_km_l": 18.9,
        "boot_space_l": 137,
        "maintenance_level": "Low",
        "best_for": ["large family", "7-seater", "budget family", "school runs", "fuel saving"],
        "pros": [
            "Affordable seven-seater",
            "Efficient for an MPV",
            "Modern safety features",
            "Easy ownership cost",
        ],
        "cons": [
            "Boot space is limited when all seats are in use",
            "Not intended for sporty driving",
        ],
        "why_this_car": "The Alza is ideal when you need seven seats, manageable monthly cost, and good fuel efficiency for family use.",
        "usage_recommendation": "Recommended for growing families who want practical seating for daily errands and weekend trips.",
        "maintenance_advice": [
            "Monitor tyre pressure carefully when the car is fully loaded.",
            "Fold and operate seats gently to keep cabin mechanisms in good shape.",
            "Follow routine servicing to maintain D-CVT smoothness.",
            "Check rear air-conditioning performance if carrying many passengers often.",
        ],
    },
]


GREETING_KEYWORDS = {"hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"}
MAINTENANCE_KEYWORDS = {"maintain", "maintenance", "service", "repair", "engine oil", "tyre", "battery", "brake"}
COMPARE_KEYWORDS = {"compare", "comparison", "versus", "vs"}
WHY_KEYWORDS = {"why", "explain", "reason", "why this car"}
USAGE_KEYWORDS = {"usage", "recommend", "recommendation", "daily", "commute", "highway", "city", "family", "student"}
SEAT_KEYWORDS = {"seat", "seats", "seater", "7 seater", "5 seater"}
INFO_KEYWORDS = {"info", "information", "details", "spec", "specification", "about"}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def find_car_by_name(user_text: str) -> Optional[Dict]:
    normalized = normalize_text(user_text)
    for car in CAR_DATABASE:
        if normalize_text(car["name"]) in normalized:
            return car
    for car in CAR_DATABASE:
        brand_model = normalize_text(" ".join(car["name"].split()[:2]))
        if brand_model in normalized:
            return car
    return None


def extract_two_cars(user_text: str) -> List[Dict]:
    normalized = normalize_text(user_text)
    matches = []
    for car in CAR_DATABASE:
        if normalize_text(car["name"]) in normalized:
            matches.append(car)
    if len(matches) >= 2:
        return matches[:2]
    for car in CAR_DATABASE:
        brand_model = normalize_text(" ".join(car["name"].split()[:2]))
        if brand_model in normalized and car not in matches:
            matches.append(car)
    return matches[:2]


def format_currency(value: int) -> str:
    return f"RM {value:,.0f}"


def format_car_card(car: Dict) -> str:
    return (
        f"**{car['name']}**\n\n"
        f"- Brand: {car['brand']}\n"
        f"- Type: {car['type']}\n"
        f"- Price: {format_currency(car['price_rm'])}\n"
        f"- Seats: {car['seats']}\n"
        f"- Transmission: {car['transmission']}\n"
        f"- Fuel: {car['fuel_type']}\n"
        f"- Fuel economy: {car['fuel_economy_km_l']} km/L\n"
        f"- Boot space: {car['boot_space_l']} L\n"
        f"- Maintenance level: {car['maintenance_level']}\n"
        f"- Best for: {', '.join(car['best_for'])}"
    )


def greeting_response() -> str:
    return (
        "Hello! I am your Malaysian Car Advisory Chatbot. "
        "I can help with car information, explain why a car suits you, compare cars, suggest cars by driving usage, recommend by seat count, and give maintenance advice."
    )


def explain_why_car(car: Dict) -> str:
    pros = "\n".join([f"- {item}" for item in car["pros"][:3]])
    return (
        f"**Why choose {car['name']}?**\n\n"
        f"{car['why_this_car']}\n\n"
        f"Top strengths:\n{pros}"
    )


def compare_cars(car1: Dict, car2: Dict) -> str:
    better_price = car1["name"] if car1["price_rm"] < car2["price_rm"] else car2["name"]
    better_economy = car1["name"] if car1["fuel_economy_km_l"] > car2["fuel_economy_km_l"] else car2["name"]
    more_seats = car1["name"] if car1["seats"] > car2["seats"] else car2["name"]
    larger_boot = car1["name"] if car1["boot_space_l"] > car2["boot_space_l"] else car2["name"]

    return (
        f"**Car Comparison: {car1['name']} vs {car2['name']}**\n\n"
        f"| Category | {car1['name']} | {car2['name']} |\n"
        f"|---|---|---|\n"
        f"| Price | {format_currency(car1['price_rm'])} | {format_currency(car2['price_rm'])} |\n"
        f"| Type | {car1['type']} | {car2['type']} |\n"
        f"| Seats | {car1['seats']} | {car2['seats']} |\n"
        f"| Fuel Economy | {car1['fuel_economy_km_l']} km/L | {car2['fuel_economy_km_l']} km/L |\n"
        f"| Boot Space | {car1['boot_space_l']} L | {car2['boot_space_l']} L |\n"
        f"| Maintenance Level | {car1['maintenance_level']} | {car2['maintenance_level']} |\n\n"
        f"Quick summary:\n"
        f"- Better price value: {better_price}\n"
        f"- Better fuel economy: {better_economy}\n"
        f"- More seating capacity: {more_seats}\n"
        f"- Larger boot space: {larger_boot}"
    )


def recommend_by_usage(user_text: str) -> str:
    normalized = normalize_text(user_text)
    recommendations = []

    if any(word in normalized for word in ["city", "traffic", "daily", "commute", "student"]):
        recommendations = [car for car in CAR_DATABASE if "city driving" in car["best_for"] or "students" in car["best_for"]]
        reason = "For city driving and daily commuting, fuel efficiency, low maintenance, and easy parking matter most."
    elif any(word in normalized for word in ["family", "kids", "school", "large family"]):
        recommendations = [car for car in CAR_DATABASE if car["seats"] >= 7 or "family" in car["best_for"]]
        reason = "For family use, practical seating, comfort, and cargo flexibility are usually the main priorities."
    elif any(word in normalized for word in ["highway", "balik kampung", "long distance", "road trip"]):
        recommendations = [car for car in CAR_DATABASE if "highway driving" in car["best_for"] or "road trips" in car["best_for"]]
        reason = "For highway usage, stability, comfort, and enough power for overtaking are important."
    elif any(word in normalized for word in ["ehailing", "grab"]):
        recommendations = [car for car in CAR_DATABASE if "e-hailing" in car["best_for"]]
        reason = "For e-hailing, low fuel cost, reliable servicing, and passenger practicality are key."
    else:
        recommendations = sorted(CAR_DATABASE, key=lambda x: (x["price_rm"], -x["fuel_economy_km_l"]))[:3]
        reason = "Without a specific driving pattern, these are balanced options with practical ownership value."

    top = recommendations[:3]
    lines = [reason, ""]
    for car in top:
        lines.append(
            f"- **{car['name']}**: {car['usage_recommendation']} Price: {format_currency(car['price_rm'])}."
        )
    return "\n".join(lines)


def recommend_by_seats(user_text: str) -> str:
    normalized = normalize_text(user_text)
    seat_match = re.search(r"(\d+)\s*-?\s*seat|\b(\d+)\s*-?\s*seater", normalized)
    desired_seats = None
    if seat_match:
        desired_seats = int(next(group for group in seat_match.groups() if group))
    elif "family" in normalized or "large" in normalized:
        desired_seats = 7
    else:
        desired_seats = 5

    matches = [car for car in CAR_DATABASE if car["seats"] == desired_seats]
    if not matches:
        return f"I could not find a {desired_seats}-seat car in the current dataset."

    lines = [f"Here are suitable **{desired_seats}-seat** options:"]
    for car in matches[:4]:
        lines.append(
            f"- **{car['name']}**: {car['type']}, {format_currency(car['price_rm'])}, best for {', '.join(car['best_for'][:3])}."
        )
    return "\n".join(lines)


def maintenance_response(car: Optional[Dict]) -> str:
    if car:
        tips = "\n".join([f"- {tip}" for tip in car["maintenance_advice"]])
        return f"**Maintenance advice for {car['name']}**\n\n{tips}"

    general_tips = [
        "Follow the manufacturer service schedule and keep service records.",
        "Check tyre pressure once a month and before long trips.",
        "Inspect engine oil, coolant, brake fluid, and washer fluid regularly.",
        "Test battery health before rainy season and long-distance travel.",
        "Replace worn wipers and monitor brake condition for safety.",
    ]
    tips = "\n".join([f"- {tip}" for tip in general_tips])
    return f"**General maintenance advice for Malaysian car owners**\n\n{tips}"


def car_info_response(car: Dict) -> str:
    pros = "\n".join([f"- {item}" for item in car["pros"]])
    cons = "\n".join([f"- {item}" for item in car["cons"]])
    return (
        f"{format_car_card(car)}\n\n"
        f"**Advantages**\n{pros}\n\n"
        f"**Things to consider**\n{cons}"
    )


def get_chatbot_response(user_text: str) -> str:
    normalized = normalize_text(user_text)
    selected_car = find_car_by_name(user_text)

    if any(keyword in normalized for keyword in GREETING_KEYWORDS):
        return greeting_response()

    if any(keyword in normalized for keyword in COMPARE_KEYWORDS):
        cars = extract_two_cars(user_text)
        if len(cars) == 2:
            return compare_cars(cars[0], cars[1])
        return "Please mention two car models from the list, for example: compare Perodua Myvi 1.5 AV vs Proton Saga 1.3 Premium S."

    if any(keyword in normalized for keyword in WHY_KEYWORDS):
        if selected_car:
            return explain_why_car(selected_car)
        return "Please tell me which car you want explained, for example: why should I choose Perodua Alza 1.5 AV?"

    if any(keyword in normalized for keyword in MAINTENANCE_KEYWORDS):
        return maintenance_response(selected_car)

    if any(keyword in normalized for keyword in SEAT_KEYWORDS):
        return recommend_by_seats(user_text)

    if any(keyword in normalized for keyword in USAGE_KEYWORDS):
        return recommend_by_usage(user_text)

    if selected_car or any(keyword in normalized for keyword in INFO_KEYWORDS):
        if selected_car:
            return car_info_response(selected_car)
        return "Please mention a car model name so I can show its details."

    return (
        "I can help with:\n"
        "- Greetings\n"
        "- Car information\n"
        "- Why this car explanation\n"
        "- Car comparison\n"
        "- Driving usage recommendations\n"
        "- Seat-based recommendations\n"
        "- Maintenance advice\n\n"
        "Try asking something like:\n"
        "- Tell me about Proton X50 1.5 TGDi Flagship\n"
        "- Why should I choose Perodua Myvi 1.5 AV?\n"
        "- Compare Honda City 1.5 RS e:HEV vs Toyota Corolla Cross 1.8V\n"
        "- Recommend a car for city driving\n"
        "- Suggest a 7-seater car\n"
        "- Maintenance advice for Perodua Alza 1.5 AV"
    )


def build_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(CAR_DATABASE)
    return df[["name", "brand", "type", "price_rm", "seats", "transmission", "fuel_type", "fuel_economy_km_l", "maintenance_level"]]


def filter_cars(max_budget: int, seats_needed: int, car_type: str) -> List[Dict]:
    results = []
    for car in CAR_DATABASE:
        if car["price_rm"] <= max_budget and car["seats"] >= seats_needed:
            if car_type == "Any" or car["type"] == car_type:
                results.append(car)
    return sorted(results, key=lambda x: (x["price_rm"], -x["fuel_economy_km_l"]))


def default_welcome_message() -> str:
    return (
        "Welcome to MyCar Advisor Malaysia. Ask me about car details, comparisons, why a car suits you, driving-use recommendations, seat-based suggestions, or maintenance tips."
    )


def build_chat_title(messages: List[Dict]) -> str:
    for message in messages:
        if message["role"] == "user":
            title = message["content"].strip()
            return title[:40] + "..." if len(title) > 40 else title
    return "New chat"


def create_chat_session(messages: Optional[List[Dict]] = None) -> Dict:
    session_messages = messages or [{"role": "assistant", "content": default_welcome_message()}]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = st.session_state.next_chat_id
    st.session_state.next_chat_id += 1
    return {
        "id": chat_id,
        "title": build_chat_title(session_messages),
        "timestamp": timestamp,
        "messages": [dict(message) for message in session_messages],
    }


def sync_active_chat_session() -> None:
    active_chat_id = st.session_state.current_chat_id
    for chat in st.session_state.chat_sessions:
        if chat["id"] == active_chat_id:
            chat["messages"] = [dict(message) for message in st.session_state.messages]
            chat["title"] = build_chat_title(chat["messages"])
            chat["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break


def start_new_chat() -> None:
    new_chat = create_chat_session()
    st.session_state.chat_sessions.insert(0, new_chat)
    st.session_state.current_chat_id = new_chat["id"]
    st.session_state.messages = [dict(message) for message in new_chat["messages"]]


def load_chat(chat_id: int) -> None:
    for chat in st.session_state.chat_sessions:
        if chat["id"] == chat_id:
            st.session_state.current_chat_id = chat_id
            st.session_state.messages = [dict(message) for message in chat["messages"]]
            break


def clear_chat_history() -> None:
    st.session_state.chat_sessions = []
    start_new_chat()


def initialize_session() -> None:
    if "next_chat_id" not in st.session_state:
        st.session_state.next_chat_id = 1
    if "chat_sessions" not in st.session_state:
        first_chat = create_chat_session()
        st.session_state.chat_sessions = [first_chat]
        st.session_state.current_chat_id = first_chat["id"]
        st.session_state.messages = [dict(message) for message in first_chat["messages"]]
    elif "messages" not in st.session_state or "current_chat_id" not in st.session_state:
        latest_chat = st.session_state.chat_sessions[0]
        st.session_state.current_chat_id = latest_chat["id"]
        st.session_state.messages = [dict(message) for message in latest_chat["messages"]]


def sidebar_ui() -> None:
    st.sidebar.title("MyCar Advisor Malaysia")
    st.sidebar.caption("FYP Streamlit chatbot for Malaysian car owners")

    st.sidebar.subheader("Chat history")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("New chat", use_container_width=True):
            start_new_chat()
            st.rerun()
    with col2:
        if st.button("Clear history", use_container_width=True):
            clear_chat_history()
            st.rerun()

    for chat in st.session_state.chat_sessions:
        button_label = f"{chat['title']}\n{chat['timestamp']}"
        button_type = "primary" if chat["id"] == st.session_state.current_chat_id else "secondary"
        if st.sidebar.button(button_label, key=f"chat_{chat['id']}", use_container_width=True, type=button_type):
            load_chat(chat["id"])
            st.rerun()

    max_budget = st.sidebar.slider("Maximum budget (RM)", 40000, 150000, 90000, 5000)
    seats_needed = st.sidebar.selectbox("Minimum seats", [4, 5, 7], index=1)
    car_type = st.sidebar.selectbox("Preferred type", ["Any", "Hatchback", "Sedan", "SUV", "MPV"])

    st.sidebar.subheader("Quick recommendations")
    results = filter_cars(max_budget, seats_needed, car_type)
    if results:
        for car in results[:3]:
            st.sidebar.markdown(
                f"**{car['name']}**  \n{format_currency(car['price_rm'])} | {car['seats']} seats | {car['type']}"
            )
    else:
        st.sidebar.info("No cars match the current filters.")

    st.sidebar.subheader("Suggested prompts")
    prompt_examples = [
        "Hello",
        "Tell me about Perodua Myvi 1.5 AV",
        "Why should I choose Honda City 1.5 RS e:HEV?",
        "Compare Proton X50 1.5 TGDi Flagship vs Toyota Corolla Cross 1.8V",
        "Recommend a car for family use",
        "Suggest a 7-seater car",
        "Maintenance advice for Proton Saga 1.3 Premium S",
    ]
    for example in prompt_examples:
        st.sidebar.code(example)


def main_ui() -> None:
    st.title("MyCar Advisor Malaysia")
    st.write(
        "A Streamlit chatbot for Malaysian car owners. This demo is designed for public sharing and covers greetings, car information, why-this-car explanations, car comparison, driving usage recommendations, seat-based recommendations, and maintenance advice."
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Chatbot")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_prompt = st.chat_input("Ask about Malaysian cars...")
        if user_prompt:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            response = get_chatbot_response(user_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            sync_active_chat_session()
            with st.chat_message("assistant"):
                st.markdown(response)

    with col2:
        st.subheader("Car Dataset")
        st.dataframe(build_dataframe(), use_container_width=True, hide_index=True)

        st.subheader("Feature Coverage")
        st.markdown(
            "- Greetings function\n"
            "- Car information function\n"
            "- Why this car explanation\n"
            "- Car comparison function\n"
            "- Driving usage recommendations\n"
            "- Seat-based function\n"
            "- Maintenance advice"
        )

        st.subheader("Public Deployment")
        st.markdown(
            "To make this chatbot public, upload this project to GitHub and deploy it with Streamlit Community Cloud. "
            "After deployment, Streamlit will generate a shareable public link."
        )


def main() -> None:
    initialize_session()
    sidebar_ui()
    main_ui()


if __name__ == "__main__":
    main()
