import java.util.Date;

class Rental {
    Movie _movie;
    private int _daysRented;
    public Rental(Movie movie, DateRange dateRange) {
        _movie = movie;
        _daysRented = (int)((dateRange.getEnd().getTime() - dateRange.getStart().getTime()) / (1000 * 60 * 60 * 24));
    }
    public int getDaysRented() {
        return _daysRented;
    }
    public int getPriceCode(){
        return _movie.getPriceCode();
    }
    public String getTitle(){
        return _movie.getTitle();
    }
    public double getCharge(){
        return _movie._priceCode.getCharge(_daysRented);
    }
    public int getFrequentRenterPoints(){
        return _movie.getFrequentRenterPoints(_daysRented);
    }

    static class DateRange {
        private final Date start;
        private final Date end;

        DateRange(Date start, Date end) {
            this.start = start;
            this.end = end;
        }

        public Date getStart() {
            return start;
        }

        public Date getEnd() {
            return end;
        }
    }
}
