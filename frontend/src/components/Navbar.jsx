import React, { useState } from "react";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import HomeIcon from "@mui/icons-material/Home";
import DirectionsBikeIcon from "@mui/icons-material/DirectionsBike";
import LeaderboardIcon from "@mui/icons-material/Leaderboard";
import SettingsIcon from "@mui/icons-material/Settings";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const [value, setValue] = useState(0);
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <BottomNavigation
      value={value}
      onChange={(event, newValue) => setValue(newValue)}
      sx={{
        position: "fixed",
        bottom: 0,
        width: "100%",
        backgroundColor: "navy", 
        color: "white",
        zIndex:1200,
      }}
    >
      <BottomNavigationAction
        label="Start"
        icon={<HomeIcon />}
        onClick={() => handleNavigation("/dashboard")}
        sx={{
          color: value === 0 ? "navy" : "white",
          backgroundColor: value === 0 ? "white" : "transparent", 
          "&:hover": {
            backgroundColor: "white", 
          },
        }}
      />
      <BottomNavigationAction
        label="Przejazdy"
        icon={<DirectionsBikeIcon />}
        onClick={() => handleNavigation("/rides")}
        sx={{
          color: value === 1 ? "navy" : "white",
          backgroundColor: value === 1 ? "white" : "transparent", 
          "&:hover": {
            backgroundColor: "white", 
          },
        }}
      />
      <BottomNavigationAction
        label="Ranking"
        icon={<LeaderboardIcon />}
        onClick={() => handleNavigation("/ranking")}
        sx={{
          color: value === 2 ? "navy" : "white",
          backgroundColor: value === 2 ? "white" : "transparent", 
          "&:hover": {
            backgroundColor: "white", 
          },
        }}
      />
      <BottomNavigationAction
        label="Opcje"
        icon={<SettingsIcon />}
        onClick={() => handleNavigation("/settings")}
        sx={{
          color: value === 3 ? "navy" : "white",
          backgroundColor: value === 3 ? "white" : "transparent", 
          "&:hover": {
            backgroundColor: "white", 
          },
        }}
      />
    </BottomNavigation>
  );
};

export default Navbar;