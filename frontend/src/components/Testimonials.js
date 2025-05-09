import React from 'react';
import '../style/components/Testimonials.css';

const testimonialsData = [
  {
    name: 'Abhay.',
    location: 'New York',
    text: 'AI Doctor helped me understand my symptoms better than my local clinic. Highly recommend!',
    rating: 5
  },
  {
    name: 'Sarvesh.',
    location: 'San Francisco',
    text: 'The symptom checker is incredibly accurate. It saved me a trip to the ER!',
    rating: 5
  },
  {
    name: 'Babulal.',
    location: 'Chicago',
    text: 'I use AI Doctor regularly to track my health. The insights are always helpful.',
    rating: 4.5
  }
];

const Testimonials = () => {
  return (
    <section className="testimonials-section">
      <h2>OUR USERS SAY</h2>
      <div className="testimonials-grid">
        {testimonialsData.map((testimonial, index) => (
          <div className="testimonial-card" key={index}>
            <div className="testimonial-rating">
              {'★'.repeat(Math.floor(testimonial.rating))}
              {testimonial.rating % 1 !== 0 && '½'}
            </div>
            <p className="testimonial-text">"{testimonial.text}"</p>
            <div className="testimonial-author">
              <span className="name">{testimonial.name}</span>
              <span className="location">{testimonial.location}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Testimonials;
