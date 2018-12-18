public class Movie {
    public static final int CHILDRENS = 2;
    public static final int REGULAR = 0;
    public static final int NEW_RELEASE = 1;
    protected String _title;
    protected Price _priceCode;

    public Movie(String title, int priceCode) {
        _title = title;
        setPriceCode(priceCode);
    }

    public String getTitle() {
        return _title;
    }


    public int getPriceCode() {
        return _priceCode.getPriceCode();
    }

    public void setPriceCode(int priceCode) {
        switch (priceCode) {
            case REGULAR:
                _priceCode= new RegularPrice();
                break;
            case CHILDRENS:
                _priceCode= new ChildrensPrice();
                break;
            case NEW_RELEASE:
                _priceCode = new NewReleasePrice();
                break;
            default:
                throw new IllegalArgumentException("Incorrect Price Code");
        }
    }

    int getFrequentRenterPoints(int daysRented) {

        return _priceCode.getFrequentRenterPoints(daysRented);
    }

    public class ChildrensPrice extends Price {
        public int getPriceCode() {
            return Movie.CHILDRENS;
        }
        @Override
        public double getCharge(int daysRented){
            double result = 0;
            result += 1.5;
            if (daysRented > 3) {
                result += (daysRented - 3) * 1.5;
            }
            return result;
        }
    }

    public class NewReleasePrice extends Price {
        public int getPriceCode() {
            return Movie.NEW_RELEASE;
        }
        @Override
        public double getCharge(int daysRented){
            return daysRented * 3;
        }
        @Override
        public int getFrequentRenterPoints(int daysRented){
            if(daysRented>1){
                return 2;
            }else{
                return 1;
            }
        }
    }

    public class RegularPrice extends Price {
        public int getPriceCode() {
            return Movie.REGULAR;
        }
        @Override
        public double getCharge(int daysRented){
            double result = 0;
            result += 2;
            if (daysRented > 2) {
                result += (daysRented - 2) * 1.5;
            }
            return result;
        }
    }

}
