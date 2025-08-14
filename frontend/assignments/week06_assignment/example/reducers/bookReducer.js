// Action types
export const ACTION_TYPES = {
  ADD_BOOK: 'ADD_BOOK',
  DELETE_BOOK: 'DELETE_BOOK',
  UPDATE_BOOK: 'UPDATE_BOOK',
  TOGGLE_FAVORITE: 'TOGGLE_FAVORITE',
  UPDATE_STATUS: 'UPDATE_STATUS',
  LOAD_BOOKS: 'LOAD_BOOKS',
  SET_SEARCH_TERM: 'SET_SEARCH_TERM',
  SET_FILTER_STATUS: 'SET_FILTER_STATUS',
  SET_FILTER_RATING: 'SET_FILTER_RATING',
  SET_SHOW_FAVORITES_ONLY: 'SET_SHOW_FAVORITES_ONLY'
};

// Initial state
export const initialState = {
  books: [],
  searchTerm: '',
  filterStatus: 'all', // all, toRead, reading, completed
  filterRating: 0, // 0 means show all
  showFavoritesOnly: false
};

// Reducer function
export function bookReducer(state, action) {
  switch (action.type) {
    case ACTION_TYPES.ADD_BOOK:
      return {
        ...state,
        books: [action.payload, ...state.books]
      };
    
    case ACTION_TYPES.DELETE_BOOK:
      return {
        ...state,
        books: state.books.filter(book => book.id !== action.payload)
      };
    
    case ACTION_TYPES.UPDATE_BOOK:
      return {
        ...state,
        books: state.books.map(book =>
          book.id === action.payload.id ? action.payload : book
        )
      };
    
    case ACTION_TYPES.TOGGLE_FAVORITE:
      return {
        ...state,
        books: state.books.map(book =>
          book.id === action.payload
            ? { ...book, isFavorite: !book.isFavorite }
            : book
        )
      };
    
    case ACTION_TYPES.UPDATE_STATUS:
      return {
        ...state,
        books: state.books.map(book =>
          book.id === action.payload.id
            ? { ...book, status: action.payload.status }
            : book
        )
      };
    
    case ACTION_TYPES.LOAD_BOOKS:
      return {
        ...state,
        books: action.payload
      };
    
    case ACTION_TYPES.SET_SEARCH_TERM:
      return {
        ...state,
        searchTerm: action.payload
      };
    
    case ACTION_TYPES.SET_FILTER_STATUS:
      return {
        ...state,
        filterStatus: action.payload
      };
    
    case ACTION_TYPES.SET_FILTER_RATING:
      return {
        ...state,
        filterRating: action.payload
      };
    
    case ACTION_TYPES.SET_SHOW_FAVORITES_ONLY:
      return {
        ...state,
        showFavoritesOnly: action.payload
      };
    
    default:
      return state;
  }
}