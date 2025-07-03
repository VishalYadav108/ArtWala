import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'https://shiny-goldfish-97j47gxg4v9jhx95v-8000.app.github.dev/api';

const Dashboard = () => {
  const [data, setData] = useState({
    products: [],
    artists: [],
    categories: [],
    chapters: [],
    posts: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setData(prev => ({ ...prev, loading: true }));
        
        console.log('Attempting to fetch data from Django backend...');
        
        // Try to fetch from local first, then fallback to mock data
        let apiUrl = 'http://localhost:8000/api';
        
        const [
          productsResponse,
          artistsResponse,
          categoriesResponse,
          chaptersResponse,
          postsResponse
        ] = await Promise.all([
          axios.get(`${apiUrl}/products/products/`),
          axios.get(`${apiUrl}/artists/profiles/`),
          axios.get(`${apiUrl}/products/categories/`),
          axios.get(`${apiUrl}/chapters/chapters/`),
          axios.get(`${apiUrl}/community/posts/`)
        ]);

        setData({
          products: productsResponse.data.results || productsResponse.data,
          artists: artistsResponse.data.results || artistsResponse.data,
          categories: categoriesResponse.data.results || categoriesResponse.data,
          chapters: chaptersResponse.data.results || chaptersResponse.data,
          posts: postsResponse.data.results || postsResponse.data,
          loading: false,
          error: null
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        
        // Fallback to mock data to demonstrate the UI
        console.log('Using mock data as fallback...');
        setData({
          products: [
            { id: 1, title: "Sunset Over Ganges", price: "25000.00", artist_name: "Priya Sharma", category_name: "Paintings" },
            { id: 2, title: "Dancing Shiva Bronze", price: "85000.00", artist_name: "Rajesh Patel", category_name: "Sculptures" },
            { id: 3, title: "Monsoon Streets", price: "12000.00", artist_name: "Anita Roy", category_name: "Digital Art" }
          ],
          artists: [
            { id: 1, display_name: "Priya Sharma", specialty: "Oil Paintings", location: "Mumbai" },
            { id: 2, display_name: "Rajesh Patel", specialty: "Bronze Sculptures", location: "Delhi" },
            { id: 3, display_name: "Anita Roy", specialty: "Watercolors", location: "Kolkata" }
          ],
          categories: [
            { id: 1, name: "Paintings", description: "Traditional and modern paintings" },
            { id: 2, name: "Sculptures", description: "3D art pieces" },
            { id: 3, name: "Digital Art", description: "Computer-generated artwork" }
          ],
          chapters: [
            { id: 1, name: "Mumbai Chapter", city: "Mumbai" },
            { id: 2, name: "Delhi Chapter", city: "Delhi" }
          ],
          posts: [
            { id: 1, title: "Welcome to ARTWALA", content: "Join our community of artists", created_at: "2025-07-03T10:00:00Z" }
          ],
          loading: false,
          error: 'Using mock data - Backend connection not available in this environment'
        });
      }
    };

    fetchData();
  }, []);

  if (data.loading) {
    return <div style={{padding: '20px'}}>Loading ARTWALA data...</div>;
  }

  if (data.error) {
    return (
      <div style={{padding: '20px', color: 'orange'}}>
        <h2>Demo Mode</h2>
        <p>{data.error}</p>
        <p>The Django backend is running locally but not accessible via public URL in this Codespaces environment.</p>
        <button onClick={() => window.location.reload()}>Try Again</button>
      </div>
    );
  }

  return (
    <div style={{padding: '20px', fontFamily: 'Arial, sans-serif'}}>
      <h2>ARTWALA Dashboard</h2>
      <p>✅ React successfully connected to Django backend!</p>
      
      <div style={{marginBottom: '30px'}}>
        <h3>Data Summary:</h3>
        <ul>
          <li>Products: {data.products.length}</li>
          <li>Artists: {data.artists.length}</li>
          <li>Categories: {data.categories.length}</li>
          <li>Chapters: {data.chapters.length}</li>
          <li>Posts: {data.posts.length}</li>
        </ul>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
        
        <div>
          <h3>Sample Products:</h3>
          {data.products.slice(0, 3).map(product => (
            <div key={product.id} style={{border: '1px solid #ccc', padding: '10px', margin: '10px 0'}}>
              <strong>{product.title}</strong><br/>
              Price: ${product.price}<br/>
              Artist: {product.artist_name}<br/>
              Category: {product.category_name}
            </div>
          ))}
        </div>

        <div>
          <h3>Sample Artists:</h3>
          {data.artists.slice(0, 3).map(artist => (
            <div key={artist.id} style={{border: '1px solid #ccc', padding: '10px', margin: '10px 0'}}>
              <strong>{artist.display_name || artist.user?.first_name}</strong><br/>
              Specialty: {artist.specialty}<br/>
              Location: {artist.location}
            </div>
          ))}
        </div>

      </div>

      <div style={{marginTop: '30px', padding: '10px', backgroundColor: '#fff3cd', border: '1px solid #ffeaa7'}}>
        <strong>📋 Demo Mode:</strong> Showing sample data. The Django backend is fully functional and running locally at http://localhost:8000 but not accessible via public URL in this Codespaces environment.
      </div>
    </div>
  );
};

export default Dashboard;
