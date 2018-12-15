public class Movie {
    public static final int CHILDRENS = 2;
    public static final int REGULAR = 0;
    public static final int NEW_RELEASE = 1;
    protected String _title;
    protected int _priceCode;

    public Movie(String title,int priceCode) {
        _priceCode = priceCode;
        _title = title;
    }
    public String getTitle() {
        return _title;
    }
    public void setTitle(String title) {
        _title = title;
    }
    public int getPriceCode() {
        return _priceCode;
    }
    public void setPriceCode(int pc) {
        _priceCode = pc;
    }
}
