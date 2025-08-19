import React, { createContext, useContext, useReducer, useEffect, useMemo, useCallback } from 'react';
import { bookReducer, initialState, ACTION_TYPES } from '../reducers/bookReducer';

// Create context
const BookContext = createContext();

// LocalStorage key
const STORAGE_KEY = 'readingLogBooksV2';

// Custom hook to use BookContext
export const useBooks = () => {
  const context = useContext(BookContext);
  if (!context) {
    throw new Error('useBooks must be used within a BookProvider');
  }
  return context;
};

// Provider component
export const BookProvider = ({ children }) => {
  // Initialize state from localStorage
  const getInitialState = () => {
    try {
      const savedData = localStorage.getItem(STORAGE_KEY);
      if (savedData) {
        const parsed = JSON.parse(savedData);
        return {
          ...initialState,
          books: parsed.books || []
        };
      }
    } catch (error) {
      console.error('Failed to load data from localStorage:', error);
    }
    return {
      ...initialState,
      books: [
        {
          id: 1,
          title: '클린 코드',
          author: '로버트 마틴',
          rating: 5,
          memo: '개발자라면 꼭 읽어야 할 필독서! 코드 품질에 대한 인식이 완전히 바뀌었습니다.',
          createdAt: '2024/08/01',
          status: 'completed',
          isFavorite: true
        },
        {
          id: 2,
          title: '리팩터링',
          author: '마틴 파울러',
          rating: 4,
          memo: '코드를 개선하는 체계적인 방법을 배울 수 있었습니다.',
          createdAt: '2024/08/03',
          status: 'completed',
          isFavorite: false
        }
      ]
    };
  };

  const [state, dispatch] = useReducer(bookReducer, initialState, getInitialState);

  // Save to localStorage whenever books change
  useEffect(() => {
    try {
      const dataToSave = {
        books: state.books
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToSave));
      console.log('Data saved to localStorage');
    } catch (error) {
      console.error('Failed to save data to localStorage:', error);
    }
  }, [state.books]);

  // Calculate statistics with useMemo
  const statistics = useMemo(() => {
    const totalBooks = state.books.length;
    const completedBooks = state.books.filter(book => book.status === 'completed').length;
    const averageRating = totalBooks > 0
      ? (state.books.reduce((sum, book) => sum + Number(book.rating), 0) / totalBooks).toFixed(1)
      : 0;
    const topRatedBook = state.books.reduce((top, book) => 
      (!top || book.rating > top.rating) ? book : top
    , null);
    const favoriteBooks = state.books.filter(book => book.isFavorite).length;

    return {
      totalBooks,
      completedBooks,
      averageRating,
      topRatedBook,
      favoriteBooks
    };
  }, [state.books]);

  // Filter and search books with useMemo
  const filteredBooks = useMemo(() => {
    let filtered = [...state.books];

    // Search filter
    if (state.searchTerm) {
      const searchLower = state.searchTerm.toLowerCase();
      filtered = filtered.filter(book =>
        book.title.toLowerCase().includes(searchLower) ||
        book.author.toLowerCase().includes(searchLower)
      );
    }

    // Status filter
    if (state.filterStatus !== 'all') {
      filtered = filtered.filter(book => book.status === state.filterStatus);
    }

    // Rating filter
    if (state.filterRating > 0) {
      filtered = filtered.filter(book => book.rating >= state.filterRating);
    }

    // Favorites filter
    if (state.showFavoritesOnly) {
      filtered = filtered.filter(book => book.isFavorite);
    }

    return filtered;
  }, [state.books, state.searchTerm, state.filterStatus, state.filterRating, state.showFavoritesOnly]);

  // Memoized dispatch functions
  const addBook = useCallback((book) => {
    dispatch({ type: ACTION_TYPES.ADD_BOOK, payload: book });
  }, []);

  const deleteBook = useCallback((id) => {
    dispatch({ type: ACTION_TYPES.DELETE_BOOK, payload: id });
  }, []);

  const updateBook = useCallback((book) => {
    dispatch({ type: ACTION_TYPES.UPDATE_BOOK, payload: book });
  }, []);

  const toggleFavorite = useCallback((id) => {
    dispatch({ type: ACTION_TYPES.TOGGLE_FAVORITE, payload: id });
  }, []);

  const updateStatus = useCallback((id, status) => {
    dispatch({ type: ACTION_TYPES.UPDATE_STATUS, payload: { id, status } });
  }, []);

  const setSearchTerm = useCallback((term) => {
    dispatch({ type: ACTION_TYPES.SET_SEARCH_TERM, payload: term });
  }, []);

  const setFilterStatus = useCallback((status) => {
    dispatch({ type: ACTION_TYPES.SET_FILTER_STATUS, payload: status });
  }, []);

  const setFilterRating = useCallback((rating) => {
    dispatch({ type: ACTION_TYPES.SET_FILTER_RATING, payload: rating });
  }, []);

  const setShowFavoritesOnly = useCallback((show) => {
    dispatch({ type: ACTION_TYPES.SET_SHOW_FAVORITES_ONLY, payload: show });
  }, []);

  const value = {
    // State
    books: state.books,
    searchTerm: state.searchTerm,
    filterStatus: state.filterStatus,
    filterRating: state.filterRating,
    showFavoritesOnly: state.showFavoritesOnly,
    
    // Computed
    filteredBooks,
    statistics,
    
    // Actions
    addBook,
    deleteBook,
    updateBook,
    toggleFavorite,
    updateStatus,
    setSearchTerm,
    setFilterStatus,
    setFilterRating,
    setShowFavoritesOnly,
    
    // Raw dispatch (if needed)
    dispatch
  };

  return <BookContext.Provider value={value}>{children}</BookContext.Provider>;
};