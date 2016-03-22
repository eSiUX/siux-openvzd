changelog:
	@rm -f .deb-changelog
	@head -1 debian/changelog | cut -d " " -f1 | tr -d '\n' > .deb-changelog
	@echo -n " (" >> .deb-changelog
	@head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f1,2 | tr -d '\n' >> .deb-changelog
	@echo -n "." >> .deb-changelog
	@V3=$$((`head -1 debian/changelog  | cut -d"(" -f2 | cut -d")" -f1 | cut -d"." -f3` + 1)); echo -n $${V3} >> .deb-changelog
	@echo ") unstable; urgency=low" >> .deb-changelog
	@echo >> .deb-changelog
	@echo "  * " >> .deb-changelog
	@echo >> .deb-changelog
	@echo -n " -- $$(sed -n '/^Maintainer:/s/^.*: //p' debian/control)  " >> .deb-changelog
	@date -R >> .deb-changelog
	@echo >> .deb-changelog
	@cat debian/changelog >> .deb-changelog
	@echo >> .deb-changelog
	@editor .deb-changelog
	@mv .deb-changelog debian/changelog

deb: changelog
	@debian/rules binary
	mv ../siux-openvzd*.deb /tmp/

clean:
	@debian/rules clean

