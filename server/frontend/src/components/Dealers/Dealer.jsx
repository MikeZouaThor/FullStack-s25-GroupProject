import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  let params = useParams();
  let id = params.id;
  const base_url = "/djangoapp";

  let dealer_url = `${base_url}/dealer/${id}`;
  let reviews_url = `${base_url}/dealer/${id}/reviews/`;
  let post_review = `/postreview/${id}`;

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET",
    });
    const retobj = await res.json();

    if (retobj.status === 200) {
      // retobj.dealer is an object, not array
      setDealer(retobj.dealer);
    }
  };

  const get_reviews = async () => {
    const res = await fetch(reviews_url, {
      method: "GET",
    });
    const retobj = await res.json();

    if (retobj.reviews && retobj.reviews.length > 0) {
      setReviews(retobj.reviews);
      setUnreviewed(false);
    } else {
      setUnreviewed(true);
    }
  };

  const senti_icon = (sentiment) => {
    let icon =
      sentiment === "positive"
        ? positive_icon
        : sentiment === "negative"
        ? negative_icon
        : neutral_icon;
    return icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <Link to={post_review}>
          <img
            src={review_icon}
            style={{ width: "10%", marginLeft: "10px", marginTop: "10px" }}
            alt="Post Review"
          />
        </Link>
      );
    }
  }, [id]);

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name}
          {postReview}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer["city"]}, {dealer["address"]}, Zip - {dealer["zip"]},{" "}
          {dealer["state"]}{" "}
        </h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          <text>Loading Reviews....</text>
        ) : unreviewed === true ? (
          <div>No reviews yet! </div>
        ) : (
          reviews.map((review) => (
            <div className="review_panel" key={review.id}>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
