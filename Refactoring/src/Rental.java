import java.util.Date;

class Rental extends Movie {

    private int _daysRented;
    public Rental(String title, int priceCode, Date start, Date end) {
        super(title, priceCode);
        _daysRented = (int)((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    }
    public int getDaysRented() {
        return _daysRented;
    }

}
