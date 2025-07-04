import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

// User Dashboard Component
const UserDashboard = () => {
  const [products, setProducts] = useState([]);
  const [artists, setArtists] = useState([]);
  const [forums, setForums] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [cart, setCart] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [selectedForum, setSelectedForum] = useState(null);
  const [showCart, setShowCart] = useState(false);
  const [showWishlist, setShowWishlist] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showUserProfile, setShowUserProfile] = useState(false);
  const [followedArtists, setFollowedArtists] = useState([]);
  const [joinedChapters, setJoinedChapters] = useState([]);
  const [joinedForums, setJoinedForums] = useState([]);

  useEffect(() => {
    // Fetch data from backend
    fetchProducts();
    fetchArtists();
    fetchForums();
    fetchChapters();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_BASE}/products/products/`);
      console.log('Products API response:', response.data);
      
      // Handle both paginated and direct array responses
      let productsData = [];
      if (response.data.results) {
        productsData = response.data.results;
      } else if (Array.isArray(response.data)) {
        productsData = response.data;
      } else {
        console.warn('Unexpected products API response format:', response.data);
        productsData = [];
      }
      
      setProducts(productsData);
    } catch (error) {
      console.error('Error fetching products:', error);
      setProducts([]); // No mock data - only real data
    }
  };

  const fetchArtists = async () => {
    try {
      const response = await axios.get(`${API_BASE}/artists/profiles/`);
      console.log('Artists API response:', response.data);
      
      // Handle both paginated and direct array responses
      let artistsData = [];
      if (response.data.results) {
        artistsData = response.data.results;
      } else if (Array.isArray(response.data)) {
        artistsData = response.data;
      } else {
        console.warn('Unexpected artists API response format:', response.data);
        artistsData = [];
      }
      
      setArtists(artistsData);
    } catch (error) {
      console.error('Error fetching artists:', error);
      setArtists([]); // No mock data - only real data
    }
  };

  const fetchForums = async () => {
    try {
      const response = await axios.get(`${API_BASE}/community/forums/`);
      console.log('Forums API response:', response.data);
      
      // Handle both paginated and direct array responses
      let forumsData = [];
      if (response.data.results) {
        forumsData = response.data.results;
      } else if (Array.isArray(response.data)) {
        forumsData = response.data;
      } else {
        console.warn('Unexpected forums API response format:', response.data);
        forumsData = [];
      }
      
      setForums(forumsData);
    } catch (error) {
      console.error('Error fetching forums:', error);
      setForums([]); // No mock data - only real data
    }
  };

  const fetchChapters = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chapters/chapters/`);
      console.log('Chapters API response:', response.data);
      
      // Handle both paginated and direct array responses
      let chaptersData = [];
      if (response.data.results) {
        chaptersData = response.data.results;
      } else if (Array.isArray(response.data)) {
        chaptersData = response.data;
      } else {
        console.warn('Unexpected chapters API response format:', response.data);
        chaptersData = [];
      }
      
      setChapters(chaptersData);
    } catch (error) {
      console.error('Error fetching chapters:', error);
      setChapters([]); // No mock data - only real data
    }
  };

  const addToCart = (product) => {
    const productInCart = cart.find(item => item.id === product.id);
    if (productInCart) {
      alert(`${product.title} is already in your cart!`);
      return;
    }
    
    const newCart = [...cart, {...product, quantity: 1}];
    setCart(newCart);
    alert(`${product.title} added to cart!`);
  };

  const removeFromCart = (productId) => {
    const newCart = cart.filter(item => item.id !== productId);
    setCart(newCart);
  };

  const addToWishlist = (product) => {
    const productInWishlist = wishlist.find(item => item.id === product.id);
    if (productInWishlist) {
      alert(`${product.title} is already in your wishlist!`);
      return;
    }
    
    const newWishlist = [...wishlist, product];
    setWishlist(newWishlist);
    alert(`${product.title} added to wishlist!`);
  };

  const removeFromWishlist = (productId) => {
    const newWishlist = wishlist.filter(item => item.id !== productId);
    setWishlist(newWishlist);
  };

  const viewArtistProfile = (artist) => {
    setSelectedArtist(artist);
    window.scrollTo(0, 0);
  };

  const joinForumDiscussion = (forum) => {
    setSelectedForum(forum);
    window.scrollTo(0, 0);
  };

  const closeArtistProfile = () => {
    setSelectedArtist(null);
  };

  const closeForumDiscussion = () => {
    setSelectedForum(null);
  };

  const followArtist = (artistId) => {
    // Check if already following
    if (followedArtists.includes(artistId)) {
      alert('You are already following this artist!');
      return;
    }
    
    // In a real implementation, this would make an API call
    setFollowedArtists([...followedArtists, artistId]);
    alert(`You are now following this artist!`);
  };

  const unfollowArtist = (artistId) => {
    // In a real implementation, this would make an API call
    setFollowedArtists(followedArtists.filter(id => id !== artistId));
    alert(`You have unfollowed this artist.`);
  };

  const joinChapter = (chapterId) => {
    // Check if already joined
    if (joinedChapters.includes(chapterId)) {
      alert('You are already a member of this chapter!');
      return;
    }
    
    // In a real implementation, this would make an API call
    setJoinedChapters([...joinedChapters, chapterId]);
    alert(`You have joined this chapter!`);
  };

  const leaveChapter = (chapterId) => {
    // In a real implementation, this would make an API call
    setJoinedChapters(joinedChapters.filter(id => id !== chapterId));
    alert(`You have left this chapter.`);
  };

  const joinForum = (forumId) => {
    // Check if already joined
    if (joinedForums.includes(forumId)) {
      alert('You are already a member of this forum!');
      return;
    }
    
    // In a real implementation, this would make an API call
    setJoinedForums([...joinedForums, forumId]);
    alert(`You have joined this forum!`);
  };

  const leaveForum = (forumId) => {
    // In a real implementation, this would make an API call
    setJoinedForums(joinedForums.filter(id => id !== forumId));
    alert(`You have left this forum.`);
  };

  const viewUserProfile = () => {
    // For demo, just show the first artist as a "user" profile
    const firstUser = artists.length > 0 ? {
      id: 1,
      name: artists[0].display_name,
      email: "user@example.com",
      joined_date: "2023-01-15",
      favorites_count: wishlist.length,
      purchases_count: 5,
      joined_chapters: joinedChapters.length,
      followed_artists: followedArtists.length
    } : {
      id: 1,
      name: "Demo User",
      email: "user@example.com",
      joined_date: "2023-01-15",
      favorites_count: wishlist.length,
      purchases_count: 5,
      joined_chapters: joinedChapters.length,
      followed_artists: followedArtists.length
    };
    
    setSelectedUser(firstUser);
    setShowUserProfile(true);
  };

  const renderCart = () => {
    return (
      <div style={{ 
        position: 'fixed', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: '80%', 
        maxWidth: '600px', 
        backgroundColor: 'white', 
        padding: '20px', 
        boxShadow: '0 0 10px rgba(0,0,0,0.2)', 
        zIndex: 1000, 
        borderRadius: '5px' 
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>Your Shopping Cart</h2>
          <button 
            onClick={() => setShowCart(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        {cart.length === 0 ? (
          <p>Your cart is empty.</p>
        ) : (
          <>
            {cart.map(item => (
              <div key={item.id} style={{ marginBottom: '10px', padding: '10px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h4>{item.title}</h4>
                  <p>Price: ₹{item.price}</p>
                </div>
                <button 
                  onClick={() => removeFromCart(item.id)} 
                  style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px' }}
                >
                  Remove
                </button>
              </div>
            ))}
            <div style={{ marginTop: '20px', textAlign: 'right' }}>
              <p><strong>Total: ₹{cart.reduce((total, item) => total + parseFloat(item.price), 0).toFixed(2)}</strong></p>
              <button 
                onClick={() => {
                  alert('Proceeding to checkout...');
                  setShowCart(false);
                }} 
                style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '3px' }}
              >
                Checkout
              </button>
            </div>
          </>
        )}
      </div>
    );
  };

  const renderWishlist = () => {
    return (
      <div style={{ 
        position: 'fixed', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: '80%', 
        maxWidth: '600px', 
        backgroundColor: 'white', 
        padding: '20px', 
        boxShadow: '0 0 10px rgba(0,0,0,0.2)', 
        zIndex: 1000, 
        borderRadius: '5px' 
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>Your Wishlist</h2>
          <button 
            onClick={() => setShowWishlist(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        {wishlist.length === 0 ? (
          <p>Your wishlist is empty.</p>
        ) : (
          <>
            {wishlist.map(item => (
              <div key={item.id} style={{ marginBottom: '10px', padding: '10px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h4>{item.title}</h4>
                  <p>Price: ₹{item.price}</p>
                </div>
                <div>
                  <button 
                    onClick={() => {
                      addToCart(item);
                      removeFromWishlist(item.id);
                    }} 
                    style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px', marginRight: '5px' }}
                  >
                    Add to Cart
                  </button>
                  <button 
                    onClick={() => removeFromWishlist(item.id)} 
                    style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px' }}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    );
  };

  const renderArtistProfile = () => {
    if (!selectedArtist) return null;
    
    return (
      <div style={{ 
        position: 'fixed', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: '80%', 
        maxWidth: '800px', 
        backgroundColor: 'white', 
        padding: '20px', 
        boxShadow: '0 0 10px rgba(0,0,0,0.2)', 
        zIndex: 1000, 
        borderRadius: '5px',
        maxHeight: '80vh',
        overflow: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>{selectedArtist.display_name}</h2>
          <button 
            onClick={closeArtistProfile} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <h3>About the Artist</h3>
            <p>{selectedArtist.bio || "This artist hasn't added a bio yet."}</p>
          </div>
          
          <div>
            <h3>Specializations</h3>
            <p>{Array.isArray(selectedArtist.specializations) 
              ? selectedArtist.specializations.join(', ') 
              : selectedArtist.specializations || 'Various art forms'}</p>
          </div>
          
          <div>
            <h3>Experience</h3>
            <p>{selectedArtist.experience_years} years of professional experience</p>
          </div>
          
          <div>
            <h3>Rating</h3>
            <p>{selectedArtist.rating}/5 from {selectedArtist.reviews_count || 0} reviews</p>
          </div>
          
          <div>
            <h3>Contact Information</h3>
            <p>Email: {selectedArtist.email || 'Not provided'}</p>
            <p>Website: {selectedArtist.website || 'Not provided'}</p>
          </div>
          
          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button 
              onClick={() => followArtist(selectedArtist.id)} 
              style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Follow Artist
            </button>
            <button 
              onClick={() => {
                alert(`Sending commission request to ${selectedArtist.display_name}...`);
              }} 
              style={{ backgroundColor: '#6c757d', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Request Commission
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderForumDiscussion = () => {
    if (!selectedForum) return null;
    
    return (
      <div style={{ 
        position: 'fixed', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: '80%', 
        maxWidth: '800px', 
        backgroundColor: 'white', 
        padding: '20px', 
        boxShadow: '0 0 10px rgba(0,0,0,0.2)', 
        zIndex: 1000, 
        borderRadius: '5px',
        maxHeight: '80vh',
        overflow: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>{selectedForum.name} Forum</h2>
          <button 
            onClick={closeForumDiscussion} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <p>{selectedForum.description}</p>
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <h3>Recent Posts</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '5px' }}>
              <h4>Welcome to the {selectedForum.name} forum!</h4>
              <p>Join the discussion about art techniques, trends, and inspirations.</p>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '12px', color: '#666' }}>
                <span>Posted by: Admin</span>
                <span>2 days ago</span>
              </div>
            </div>
            <div style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '5px' }}>
              <h4>Looking for collaboration on a mural project</h4>
              <p>I'm looking for artists interested in collaborating on a large mural project in the city center.</p>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '12px', color: '#666' }}>
                <span>Posted by: MuralArtist123</span>
                <span>5 hours ago</span>
              </div>
            </div>
          </div>
        </div>
        
        <div>
          <h3>Add Your Post</h3>
          <textarea 
            placeholder="What's on your mind?"
            style={{ width: '100%', padding: '10px', height: '100px', marginBottom: '10px', borderRadius: '5px', border: '1px solid #ddd' }}
          ></textarea>
          <button 
            onClick={() => alert('Post added to the forum!')} 
            style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
          >
            Post
          </button>
        </div>
      </div>
    );
  };

  const renderUserProfile = () => {
    if (!selectedUser || !showUserProfile) return null;
    
    return (
      <div style={{ 
        position: 'fixed', 
        top: '50%', 
        left: '50%', 
        transform: 'translate(-50%, -50%)', 
        width: '80%', 
        maxWidth: '800px', 
        backgroundColor: 'white', 
        padding: '20px', 
        boxShadow: '0 0 10px rgba(0,0,0,0.2)', 
        zIndex: 1000, 
        borderRadius: '5px',
        maxHeight: '80vh',
        overflow: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>User Profile: {selectedUser.name}</h2>
          <button 
            onClick={() => setShowUserProfile(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <h3>Account Information</h3>
            <p><strong>Email:</strong> {selectedUser.email}</p>
            <p><strong>Member Since:</strong> {selectedUser.joined_date}</p>
          </div>
          
          <div>
            <h3>Activity Summary</h3>
            <p><strong>Items in Wishlist:</strong> {wishlist.length}</p>
            <p><strong>Purchases:</strong> {selectedUser.purchases_count}</p>
            <p><strong>Joined Chapters:</strong> {selectedUser.joined_chapters}</p>
            <p><strong>Following Artists:</strong> {selectedUser.followed_artists}</p>
          </div>
          
          <div>
            <h3>Recently Viewed Products</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {products.slice(0, 3).map(product => (
                <div key={product.id} style={{ 
                  border: '1px solid #ddd', 
                  padding: '10px', 
                  borderRadius: '5px',
                  width: 'calc(33% - 10px)'
                }}>
                  <h4>{product.title}</h4>
                  <p>₹{product.price}</p>
                </div>
              ))}
            </div>
          </div>
          
          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button 
              onClick={() => {
                alert('Settings page would open here');
                setShowUserProfile(false);
              }} 
              style={{ backgroundColor: '#6c757d', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Account Settings
            </button>
            <button 
              onClick={() => {
                alert('Order history would be displayed here');
              }} 
              style={{ backgroundColor: '#17a2b8', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Order History
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>ArtWala - User Dashboard</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={viewUserProfile} 
            style={{ 
              backgroundColor: '#17a2b8', 
              color: 'white', 
              border: 'none', 
              padding: '8px 16px', 
              borderRadius: '3px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <span style={{ fontSize: '18px' }}>👤</span>
            View Profile
          </button>
          <button 
            onClick={() => setShowWishlist(true)} 
            style={{ 
              backgroundColor: '#6c757d', 
              color: 'white', 
              border: 'none', 
              padding: '8px 16px', 
              borderRadius: '3px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <span style={{ fontSize: '18px' }}>❤️</span>
            Wishlist ({wishlist.length})
          </button>
          <button 
            onClick={() => setShowCart(true)} 
            style={{ 
              backgroundColor: '#007bff', 
              color: 'white', 
              border: 'none', 
              padding: '8px 16px', 
              borderRadius: '3px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <span style={{ fontSize: '18px' }}>🛒</span>
            Cart ({cart.length})
          </button>
        </div>
      </div>
      
      {/* Products Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Featured Products</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '15px' }}>
          {Array.isArray(products) && products.length > 0 ? (
            products.map(product => (
              <div key={product.id} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
                <h3>{product.title}</h3>
                <p><strong>Price: ₹{product.price}</strong></p>
                <p>Artist: {product.artist?.display_name || product.artist}</p>
                <p>Medium: {product.medium}</p>
                <p>Dimensions: {product.dimensions}</p>
                <p>Year: {product.year_created}</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                  <span>❤️ {product.likes_count}</span>
                  <span>👁️ {product.views_count}</span>
                </div>
                {product.featured && <span style={{ 
                  backgroundColor: '#ffd700', 
                  padding: '2px 6px', 
                  borderRadius: '3px', 
                  fontSize: '12px',
                  fontWeight: 'bold',
                  display: 'inline-block',
                  marginBottom: '10px'
                }}>FEATURED</span>}
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <button 
                    onClick={() => addToCart(product)} 
                    style={{ 
                      backgroundColor: '#007bff', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>🛒</span>
                    Add to Cart
                  </button>
                  <button 
                    onClick={() => addToWishlist(product)} 
                    style={{ 
                      backgroundColor: '#6c757d', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>❤️</span>
                    Save
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '20px' }}>
              <p>No products available. Loading...</p>
            </div>
          )}
        </div>
      </div>

      {/* Artists Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Featured Artists</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '15px' }}>
          {Array.isArray(artists) && artists.length > 0 ? (
            artists.map(artist => (
              <div key={artist.id} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
                <h3>{artist.display_name}</h3>
                <p>Specializations: {Array.isArray(artist.specializations) ? artist.specializations.join(', ') : 'Various'}</p>
                <p>Rating: {artist.rating}/5</p>
                <p>Experience: {artist.experience_years} years</p>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <button 
                    onClick={() => viewArtistProfile(artist)} 
                    style={{ 
                      backgroundColor: '#17a2b8', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>👁️</span>
                    View Profile
                  </button>
                  {followedArtists.includes(artist.id) ? (
                    <button 
                      onClick={() => unfollowArtist(artist.id)} 
                      style={{ 
                        backgroundColor: '#dc3545', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>✓</span>
                      Unfollow
                    </button>
                  ) : (
                    <button 
                      onClick={() => followArtist(artist.id)} 
                      style={{ 
                        backgroundColor: '#28a745', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>+</span>
                      Follow
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '20px' }}>
              <p>No artists available. Loading...</p>
            </div>
          )}
        </div>
      </div>

      {/* Community Forums */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Community Forums</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '10px' }}>
          {Array.isArray(forums) && forums.length > 0 ? (
            forums.map(forum => (
              <div key={forum.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3>{forum.name}</h3>
                  <p>{forum.description}</p>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button 
                    onClick={() => joinForumDiscussion(forum)} 
                    style={{ 
                      backgroundColor: '#17a2b8', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>💬</span>
                    View Discussion
                  </button>
                  {joinedForums.includes(forum.id) ? (
                    <button 
                      onClick={() => leaveForum(forum.id)} 
                      style={{ 
                        backgroundColor: '#dc3545', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>✓</span>
                      Leave Forum
                    </button>
                  ) : (
                    <button 
                      onClick={() => joinForum(forum.id)} 
                      style={{ 
                        backgroundColor: '#28a745', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>+</span>
                      Join Forum
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <p>No forums available. Loading...</p>
            </div>
          )}
        </div>
      </div>

      {/* Regional Chapters */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Regional Chapters</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '15px' }}>
          {Array.isArray(chapters) && chapters.length > 0 ? (
            chapters.map(chapter => (
              <div key={chapter.id} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
                <h3>{chapter.name}</h3>
                <p>{chapter.city}, {chapter.state}</p>
                <p>{chapter.description}</p>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <button 
                    onClick={() => alert(`Viewing artists in ${chapter.name}...`)} 
                    style={{ 
                      backgroundColor: '#17a2b8', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>👁️</span>
                    View Artists
                  </button>
                  {joinedChapters.includes(chapter.id) ? (
                    <button 
                      onClick={() => leaveChapter(chapter.id)} 
                      style={{ 
                        backgroundColor: '#dc3545', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>✓</span>
                      Leave Chapter
                    </button>
                  ) : (
                    <button 
                      onClick={() => joinChapter(chapter.id)} 
                      style={{ 
                        backgroundColor: '#28a745', 
                        color: 'white', 
                        border: 'none', 
                        padding: '5px 10px', 
                        borderRadius: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '2px'
                      }}
                    >
                      <span style={{ fontSize: '14px' }}>+</span>
                      Join Chapter
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '20px' }}>
              <p>No chapters available. Loading...</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Modals */}
      {showCart && renderCart()}
      {showWishlist && renderWishlist()}
      {renderArtistProfile()}
      {renderForumDiscussion()}
      {showUserProfile && renderUserProfile()}
    </div>
  );
};

export default UserDashboard;
