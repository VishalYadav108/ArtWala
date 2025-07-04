import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

// Artist Dashboard Component
const ArtistDashboard = () => {
  const [products, setProducts] = useState([]);
  const [commissions, setCommissions] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [newProduct, setNewProduct] = useState({ 
    title: '', 
    price: '', 
    description: '', 
    medium: '', 
    dimensions: '',
    year_created: '',
    status: 'draft'
  });
  const [selectedCommission, setSelectedCommission] = useState(null);
  const [productToEdit, setProductToEdit] = useState(null);
  const [showCommissionDetails, setShowCommissionDetails] = useState(false);
  const [showEditProduct, setShowEditProduct] = useState(false);
  const [showArtistProfile, setShowArtistProfile] = useState(false);
  const [artistProfile, setArtistProfile] = useState(null);
  const [productImageUrl, setProductImageUrl] = useState('');
  const [currentArtistId, setCurrentArtistId] = useState(1); // Simulate current artist ID
  const [completedCommissions, setCompletedCommissions] = useState([]);

  useEffect(() => {
    fetchArtistProducts();
    fetchCommissions();
    fetchAnalytics();
    fetchArtistProfile();
  }, []);

  // Fetch artist profile for the "View Artist" button
  const fetchArtistProfile = async () => {
    try {
      const response = await axios.get(`${API_BASE}/artists/profiles/`);
      if (response.data && (response.data.results || Array.isArray(response.data)) && 
         ((response.data.results && response.data.results.length > 0) || 
          (Array.isArray(response.data) && response.data.length > 0))) {
        
        const profiles = response.data.results || response.data;
        setArtistProfile(profiles[0]); // Use the first artist for demo
      } else {
        // Create mock artist profile if API returns no data
        setArtistProfile({
          id: 1,
          display_name: "Demo Artist",
          bio: "This is a demo artist profile for the ArtWala platform.",
          specializations: ["Painting", "Digital Art"],
          experience_years: 5,
          rating: 4.8,
          reviews_count: 12,
          email: "artist@example.com",
          website: "https://example.com/artist",
          social_media: {
            instagram: "@demoartist",
            twitter: "@demoartist"
          }
        });
      }
    } catch (error) {
      console.error('Error fetching artist profile:', error);
      // Set mock profile on error
      setArtistProfile({
        id: 1,
        display_name: "Demo Artist",
        bio: "This is a demo artist profile for the ArtWala platform.",
        specializations: ["Painting", "Digital Art"],
        experience_years: 5,
        rating: 4.8,
        reviews_count: 12,
        email: "artist@example.com",
        website: "https://example.com/artist",
        social_media: {
          instagram: "@demoartist",
          twitter: "@demoartist"
        }
      });
    }
  };

  const fetchArtistProducts = async () => {
    try {
      const response = await axios.get(`${API_BASE}/products/products/`);
      console.log('Artist Products API response:', response.data);
      
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

  const fetchCommissions = async () => {
    try {
      const response = await axios.get(`${API_BASE}/commissions/requests/`);
      console.log('Commissions API response:', response.data);
      
      // Handle both paginated and direct array responses
      let commissionsData = [];
      if (response.data.results) {
        commissionsData = response.data.results;
      } else if (Array.isArray(response.data)) {
        commissionsData = response.data;
      } else {
        console.warn('Unexpected commissions API response format:', response.data);
        commissionsData = [];
      }
      
      setCommissions(commissionsData);
    } catch (error) {
      console.error('Error fetching commissions:', error);
      setCommissions([]); // No mock data - only real data
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API_BASE}/artists/profiles/analytics/`);
      console.log('Analytics API response:', response.data);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      // Set empty analytics if API fails
      setAnalytics({
        total_sales: 0,
        total_orders: 0,
        total_commissions: 0,
        profile_views: 0,
        products_sold: 0,
        average_rating: 0
      });
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    try {
      // In a real implementation, this would send data to the backend
      // const response = await axios.post(`${API_BASE}/products/products/`, newProduct);
      
      // For demo purposes, we'll simulate a successful response
      const mockResponse = {
        ...newProduct,
        id: products.length + 1,
        artist: "Current Artist",
        views_count: 0,
        likes_count: 0,
        created_at: new Date().toISOString(),
        status: newProduct.status || 'draft'
      };
      
      setProducts([...products, mockResponse]);
      setNewProduct({ 
        title: '', 
        price: '', 
        description: '', 
        medium: '', 
        dimensions: '',
        year_created: '',
        status: 'draft'
      });
      alert('Product added successfully!');
    } catch (error) {
      console.error('Error adding product:', error);
      alert('Error adding product. Please try again.');
    }
  };

  const handleProductUpdate = async (e) => {
    e.preventDefault();
    if (!productToEdit) return;
    
    try {
      // In a real implementation, this would update the backend
      // const response = await axios.put(`${API_BASE}/products/products/${productToEdit.id}/`, productToEdit);
      
      // For demo purposes, update the local state
      const updatedProducts = products.map(p => 
        p.id === productToEdit.id ? {...productToEdit} : p
      );
      
      setProducts(updatedProducts);
      setProductToEdit(null);
      setShowEditProduct(false);
      alert('Product updated successfully!');
    } catch (error) {
      console.error('Error updating product:', error);
      alert('Error updating product. Please try again.');
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      // In a real implementation, this would delete from the backend
      // await axios.delete(`${API_BASE}/products/products/${productId}/`);
      
      // For demo purposes, update the local state
      const updatedProducts = products.filter(p => p.id !== productId);
      setProducts(updatedProducts);
      alert('Product deleted successfully!');
    } catch (error) {
      console.error('Error deleting product:', error);
      alert('Error deleting product. Please try again.');
    }
  };

  const handleAcceptCommission = (commission) => {
    alert(`Commission '${commission.title}' accepted! You will be contacted for next steps.`);
    // In a real implementation, this would update the commission status in the backend
    const updatedCommissions = commissions.map(c => 
      c.id === commission.id ? {...c, status: 'accepted'} : c
    );
    setCommissions(updatedCommissions);
  };

  const handleDeclineCommission = (commission) => {
    if (!window.confirm('Are you sure you want to decline this commission request?')) return;
    
    alert(`Commission '${commission.title}' declined.`);
    // In a real implementation, this would update the commission status in the backend
    const updatedCommissions = commissions.map(c => 
      c.id === commission.id ? {...c, status: 'rejected'} : c
    );
    setCommissions(updatedCommissions);
  };

  const viewCommissionDetails = (commission) => {
    setSelectedCommission(commission);
    setShowCommissionDetails(true);
  };

  const editProduct = (product) => {
    setProductToEdit({...product});
    setShowEditProduct(true);
    window.scrollTo(0, 0);
  };

  const viewArtistProfile = () => {
    setShowArtistProfile(true);
  };

  const renderCommissionDetails = () => {
    if (!selectedCommission || !showCommissionDetails) return null;
    
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
          <h2>Commission Request: {selectedCommission.title}</h2>
          <button 
            onClick={() => setShowCommissionDetails(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <h3>Client Details</h3>
          <p><strong>Client:</strong> {selectedCommission.client_name}</p>
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <h3>Project Details</h3>
          <p><strong>Type:</strong> {selectedCommission.commission_type}</p>
          <p><strong>Description:</strong> {selectedCommission.description}</p>
          <p><strong>Budget:</strong> ₹{selectedCommission.budget_min} - ₹{selectedCommission.budget_max}</p>
          <p><strong>Deadline:</strong> {new Date(selectedCommission.deadline).toLocaleDateString()}</p>
          <p><strong>Status:</strong> {selectedCommission.status}</p>
          <p><strong>Dimensions:</strong> {selectedCommission.dimensions || 'Not specified'}</p>
          <p><strong>Additional Requirements:</strong> {selectedCommission.additional_requirements || 'None'}</p>
        </div>
        
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
          <button 
            onClick={() => {
              handleDeclineCommission(selectedCommission);
              setShowCommissionDetails(false);
            }} 
            style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
          >
            Decline
          </button>
          <button 
            onClick={() => {
              handleAcceptCommission(selectedCommission);
              setShowCommissionDetails(false);
            }} 
            style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
          >
            Accept Commission
          </button>
        </div>
      </div>
    );
  };

  const renderEditProductForm = () => {
    if (!productToEdit || !showEditProduct) return null;
    
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
          <h2>Edit Product: {productToEdit.title}</h2>
          <button 
            onClick={() => setShowEditProduct(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <form onSubmit={handleProductUpdate} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Product Title:</label>
            <input
              type="text"
              value={productToEdit.title}
              onChange={(e) => setProductToEdit({...productToEdit, title: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              required
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Price (₹):</label>
            <input
              type="number"
              value={productToEdit.price}
              onChange={(e) => setProductToEdit({...productToEdit, price: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              required
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Description:</label>
            <textarea
              value={productToEdit.description}
              onChange={(e) => setProductToEdit({...productToEdit, description: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px', height: '100px' }}
              required
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Medium:</label>
            <input
              type="text"
              value={productToEdit.medium || ''}
              onChange={(e) => setProductToEdit({...productToEdit, medium: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Dimensions:</label>
            <input
              type="text"
              value={productToEdit.dimensions || ''}
              onChange={(e) => setProductToEdit({...productToEdit, dimensions: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Year Created:</label>
            <input
              type="number"
              value={productToEdit.year_created || ''}
              onChange={(e) => setProductToEdit({...productToEdit, year_created: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Status:</label>
            <select
              value={productToEdit.status || 'draft'}
              onChange={(e) => setProductToEdit({...productToEdit, status: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="sold">Sold</option>
              <option value="archived">Archived</option>
            </select>
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Image URL:</label>
            <input
              type="text"
              value={productToEdit.image_url || ''}
              onChange={(e) => setProductToEdit({...productToEdit, image_url: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            />
          </div>
          
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '10px' }}>
            <button 
              type="button"
              onClick={() => setShowEditProduct(false)} 
              style={{ backgroundColor: '#6c757d', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    );
  };

  const renderArtistProfile = () => {
    if (!artistProfile || !showArtistProfile) return null;
    
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
          <h2>Artist Profile: {artistProfile.display_name}</h2>
          <button 
            onClick={() => setShowArtistProfile(false)} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <h3>About the Artist</h3>
            <p>{artistProfile.bio || "This artist hasn't added a bio yet."}</p>
          </div>
          
          <div>
            <h3>Specializations</h3>
            <p>{Array.isArray(artistProfile.specializations) 
              ? artistProfile.specializations.join(', ') 
              : artistProfile.specializations || 'Various art forms'}</p>
          </div>
          
          <div>
            <h3>Experience</h3>
            <p>{artistProfile.experience_years} years of professional experience</p>
          </div>
          
          <div>
            <h3>Rating</h3>
            <p>{artistProfile.rating}/5 from {artistProfile.reviews_count || 0} reviews</p>
          </div>
          
          <div>
            <h3>Contact Information</h3>
            <p>Email: {artistProfile.email || 'Not provided'}</p>
            <p>Website: {artistProfile.website || 'Not provided'}</p>
            {artistProfile.social_media && Object.keys(artistProfile.social_media).length > 0 && (
              <div>
                <h4>Social Media</h4>
                {Object.entries(artistProfile.social_media).map(([platform, handle]) => (
                  <p key={platform}>{platform}: {handle}</p>
                ))}
              </div>
            )}
          </div>
          
          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button 
              onClick={() => {
                alert('Editing profile...');
                setShowArtistProfile(false);
              }} 
              style={{ backgroundColor: '#6c757d', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Edit Profile
            </button>
            <button 
              onClick={() => {
                alert('Portfolio settings...');
              }} 
              style={{ backgroundColor: '#17a2b8', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '3px' }}
            >
              Portfolio Settings
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>ArtWala - Artist Dashboard</h1>
        <button 
          onClick={() => setShowArtistProfile(true)} 
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
          View Artist Profile
        </button>
      </div>
      
      {/* Analytics Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Your Statistics</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '15px' }}>
          <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', textAlign: 'center' }}>
            <h3>₹{analytics.total_sales}</h3>
            <p>Total Sales</p>
          </div>
          <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', textAlign: 'center' }}>
            <h3>{analytics.total_orders}</h3>
            <p>Total Orders</p>
          </div>
          <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', textAlign: 'center' }}>
            <h3>{analytics.total_commissions}</h3>
            <p>Commissions</p>
          </div>
          <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', textAlign: 'center' }}>
            <h3>{analytics.profile_views}</h3>
            <p>Profile Views</p>
          </div>
          <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px', textAlign: 'center' }}>
            <h3>{analytics.average_rating}/5</h3>
            <p>Average Rating</p>
          </div>
        </div>
      </div>

      {/* Add New Product Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Add New Product</h2>
        <form onSubmit={handleProductSubmit} style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '5px' }}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Product Title:</label>
            <input
              type="text"
              value={newProduct.title}
              onChange={(e) => setNewProduct({...newProduct, title: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              required
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Price (₹):</label>
            <input
              type="number"
              value={newProduct.price}
              onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              required
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Description:</label>
            <textarea
              value={newProduct.description}
              onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px', height: '100px' }}
              required
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Medium:</label>
            <input
              type="text"
              value={newProduct.medium}
              onChange={(e) => setNewProduct({...newProduct, medium: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              placeholder="E.g., Oil on canvas, Digital print, etc."
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Dimensions:</label>
            <input
              type="text"
              value={newProduct.dimensions}
              onChange={(e) => setNewProduct({...newProduct, dimensions: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              placeholder="E.g., 24x36 inches"
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Year Created:</label>
            <input
              type="number"
              value={newProduct.year_created}
              onChange={(e) => setNewProduct({...newProduct, year_created: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              placeholder="E.g., 2025"
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Status:</label>
            <select
              value={newProduct.status}
              onChange={(e) => setNewProduct({...newProduct, status: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="sold">Sold</option>
              <option value="archived">Archived</option>
            </select>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Product Image URL:</label>
            <input
              type="text"
              value={newProduct.image_url || ''}
              onChange={(e) => setNewProduct({...newProduct, image_url: e.target.value})}
              style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '3px' }}
              placeholder="https://example.com/image.jpg"
            />
          </div>
          <button type="submit" style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '3px' }}>
            Add Product
          </button>
        </form>
      </div>

      {/* My Products Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>My Products</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '15px' }}>
          {Array.isArray(products) && products.length > 0 ? (
            products.map(product => (
              <div key={product.id} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }}>
                <h3>{product.title}</h3>
                {product.image_url && (
                  <div style={{ 
                    height: '120px', 
                    background: `url(${product.image_url || 'https://via.placeholder.com/150'}) center/cover no-repeat`,
                    marginBottom: '10px',
                    borderRadius: '3px'
                  }} />
                )}
                <p><strong>Price: ₹{product.price}</strong></p>
                <p>Status: <span style={{ 
                  color: product.status === 'published' ? 'green' : product.status === 'sold' ? 'blue' : 'orange' 
                }}>{product.status || 'Draft'}</span></p>
                <p>Views: {product.views_count || 0}</p>
                <p>Medium: {product.medium || 'Not specified'}</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
                  <button 
                    onClick={() => editProduct(product)} 
                    style={{ 
                      backgroundColor: '#6c757d', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px', 
                      marginRight: '5px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                  >
                    <span style={{ fontSize: '14px' }}>✏️</span>
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDeleteProduct(product.id)} 
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
                    <span style={{ fontSize: '14px' }}>🗑️</span>
                    Delete
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '20px' }}>
              <p>No products available. Add your first product above!</p>
            </div>
          )}
        </div>
      </div>

      {/* Commission Requests Section */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Commission Requests</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '10px' }}>
          {Array.isArray(commissions) && commissions.length > 0 ? (
            commissions.map(commission => (
              <div key={commission.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3>{commission.title}</h3>
                  <span style={{ 
                    padding: '3px 8px',
                    borderRadius: '3px',
                    fontSize: '12px',
                    fontWeight: 'bold',
                    backgroundColor: 
                      commission.status === 'accepted' ? '#d4edda' : 
                      commission.status === 'rejected' ? '#f8d7da' : 
                      commission.status === 'in_progress' ? '#cce5ff' : '#fff3cd',
                    color: 
                      commission.status === 'accepted' ? '#155724' : 
                      commission.status === 'rejected' ? '#721c24' : 
                      commission.status === 'in_progress' ? '#004085' : '#856404',
                  }}>
                    {commission.status === 'accepted' ? '✓ ACCEPTED' : 
                     commission.status === 'rejected' ? '✗ DECLINED' : 
                     commission.status === 'in_progress' ? '⟳ IN PROGRESS' : '⧗ PENDING'}
                  </span>
                </div>
                <p>Budget: Up to ₹{commission.budget_max}</p>
                <p>Client: {commission.client_name}</p>
                <div style={{ display: 'flex', gap: '5px', marginTop: '10px' }}>
                  <button 
                    onClick={() => handleAcceptCommission(commission)} 
                    style={{ 
                      backgroundColor: '#28a745', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      opacity: commission.status === 'accepted' || commission.status === 'rejected' ? 0.5 : 1,
                      cursor: commission.status === 'accepted' || commission.status === 'rejected' ? 'not-allowed' : 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                    disabled={commission.status === 'accepted' || commission.status === 'rejected'}
                  >
                    <span style={{ fontSize: '14px' }}>✓</span>
                    Accept
                  </button>
                  <button 
                    onClick={() => viewCommissionDetails(commission)} 
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
                    View Details
                  </button>
                  <button 
                    onClick={() => handleDeclineCommission(commission)} 
                    style={{ 
                      backgroundColor: '#dc3545', 
                      color: 'white', 
                      border: 'none', 
                      padding: '5px 10px', 
                      borderRadius: '3px',
                      opacity: commission.status === 'accepted' || commission.status === 'rejected' ? 0.5 : 1,
                      cursor: commission.status === 'accepted' || commission.status === 'rejected' ? 'not-allowed' : 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '2px'
                    }}
                    disabled={commission.status === 'accepted' || commission.status === 'rejected'}
                  >
                    <span style={{ fontSize: '14px' }}>✗</span>
                    Decline
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <p>No commission requests available.</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Modals */}
      {renderCommissionDetails()}
      {renderEditProductForm()}
      {renderArtistProfile()}
    </div>
  );
};

export default ArtistDashboard;
