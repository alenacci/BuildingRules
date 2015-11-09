(function() {
    d3.selection.prototype.class =
        d3.selection.enter.prototype.class =
            d3.transition.prototype.class =
                function (c) {
                    this.classed(c, true);
                    return this;
                };

    d3.selection.prototype.style =
        d3.selection.enter.prototype.style =
            d3.transition.prototype.style =
                function (style) {
                    this.attr("style", style);
                    return this;
                };

    d3.selection.prototype.textAlign =
        d3.selection.enter.prototype.textAlign =
            d3.transition.prototype.textAlign =
                function (alignment) {
                    this.style("text-align: " + alignment);
                    return this;
                };

})();