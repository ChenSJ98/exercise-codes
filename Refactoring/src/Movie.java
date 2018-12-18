public class Movie {
    public static final int CHILDRENS = 2;
    public static final int REGULAR = 0;
    public static final int NEW_RELEASE = 1;
    protected String _title;
    protected int _priceCode;

    public Movie(String title, int priceCode) {
        _title = title;
        _priceCode = priceCode;
    }

    public String getTitle() {
        return _title;
    }
    public void setTitle(String t){
        _title = t;
    }
    public void setPriceCode(int p){
        _priceCode = p;
    }
    public int getPriceCode() {
        return _priceCode;
    }
}
